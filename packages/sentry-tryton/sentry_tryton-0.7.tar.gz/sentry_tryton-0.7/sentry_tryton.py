# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import pkg_resources

from raven.handlers.logging import SentryHandler
from raven.processors import Processor
from trytond import backend
from trytond.exceptions import (
    ConcurrencyException, RateLimitException, UserError, UserWarning)
from trytond.transaction import Transaction
from werkzeug.exceptions import HTTPException

__version__ = '0.7'
__all__ = ['TrytonProcessor', 'SentryTrytonHandler']


class TrytonProcessor(Processor):

    def __init__(self, client):
        super(TrytonProcessor, self).__init__(client)
        self.modules = {}
        for module in pkg_resources.WorkingSet():
            self.modules[module.key] = module.version

    def get_data(self, data, **kwargs):
        user = {}
        extra = {}
        database = None
        # Must be imported once the logging is set
        from trytond.pool import Pool
        try:
            # Must not fail if connection is not available
            pool = Pool()
        except Exception:
            pool = None
        transaction = Transaction()
        if transaction:
            user['id'] = transaction.user
            try:
                backend_name = backend.name()
            except TypeError:
                # Support for 5.6+ series
                backend_name = backend.name

            extra.update({
                'backend': backend_name,
                'context': transaction.context,
                'readonly': transaction.readonly,
                })
            if transaction.database:
                database = transaction.database.name
                extra['database'] = database
        if pool:
            try:
                User = pool.get('res.user')
                tryton_user = User(user['id'])
                user.update({
                    'username': tryton_user.rec_name,
                    'login': tryton_user.login,
                    'email': tryton_user.email,
                    })
            except Exception:
                pass
            if database:
                activated_modules = {}
                try:
                    Module = pool.get('ir.module')
                    for module in Module.search([
                                ('state', '=', 'activated'),
                                ]):
                        activated_modules[module.name] = module.version
                except Exception:
                    pass
                extra['activated_modules'] = activated_modules
        return {
            'modules': self.modules,
            'user': user,
            'extra': extra
            }


class SentryTrytonHandler(SentryHandler):

    def __init__(
            self, dsn, error_msg=None, error_description=None, extra_args=None,
            **kwargs):
        self.error_msg = error_msg
        self.error_description = error_description
        # Replace {keyword} as its not possible to use format expresions
        # when using fileConfig
        for keyword in ['event_id', 'message']:
            src = '{' + keyword + '}'
            dst = '%(' + keyword + ')s'
            if self.error_msg is not None:
                self.error_msg = self.error_msg.replace(src, dst)
            if self.error_description is not None:
                self.error_description = self.error_description.replace(
                    src, dst)
        if isinstance(extra_args, dict):
            kwargs.update(extra_args)
        super(SentryTrytonHandler, self).__init__(dsn=dsn, **kwargs)
        self.client.processors += ('sentry_tryton.TrytonProcessor',)

    def can_record(self, record):
        if record.name == 'trytond.security':
            return False
        if record.exc_info:
            exception = record.exc_info[0]
            if issubclass(exception, UserError):
                return False
            if issubclass(exception, UserWarning):
                return False
            if issubclass(exception, ConcurrencyException):
                return False
            if issubclass(exception, RateLimitException):
                return False
            if issubclass(exception, HTTPException):
                return not str(exception.code).startswith('4')
        return super(SentryTrytonHandler, self).can_record(record)

    def emit(self, record):
        event_id = super(SentryTrytonHandler, self).emit(record)
        if self.error_msg and self.can_record(record):
            message = record.message
            if record.exc_info and len(record.exc_info) > 1:
                message = str(record.exc_info[1])
            message_args = {
                    'event_id': event_id,
                    'message': message,
                    }
            msg = self.error_msg % message_args
            description = ''
            if self.error_description:
                description = self.error_description % message_args
            raise UserError(msg, description)
        return event_id
