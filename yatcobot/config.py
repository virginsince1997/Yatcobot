import logging

import confuse
import os.path
import pkg_resources
import yaml

logger = logging.getLogger(__name__)


class NumberKeywordsTemplate(confuse.Template):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def value(self, view, template=None):
        out = confuse.AttrDict()

        for key, value in view.items():
            if not isinstance(key, int):
                self.fail('Number keywords must have integer keys', view, type_error=True)
            out[key] = value.as_str_seq()

        return out

    def __repr__(self):
        return 'NumberKeywordsTemplate()'


class Config:
    template = {
        'twitter': {
            'consumer_key': confuse.String(),
            'consumer_secret': confuse.String(),
            'access_token_key': confuse.String(),
            'access_token_secret': confuse.String(),
            'min_ratelimit_percent': confuse.Integer(),

            'search': {
                'queries': confuse.TypeTemplate(list),
                'max_queue': confuse.Integer(),
                'max_quote_depth': confuse.Integer(),
                'min_quote_similarity': confuse.Number(),
                'skip_retweeted': confuse.TypeTemplate(bool),
                'filter': {
                    'min_retweets': {
                        'enabled': confuse.TypeTemplate(bool),
                        'number': confuse.Integer()
                    }
                },
                'sort': {
                    'by_keywords': {
                        'enabled': confuse.TypeTemplate(bool),
                        'keywords': confuse.StrSeq()
                    },
                    'by_age': {
                        'enabled': confuse.TypeTemplate(bool),
                    },
                    'by_retweets_count': {
                        'enabled': confuse.TypeTemplate(bool),
                    }
                }
            },

            'actions': {
                'follow': {
                    'enabled': confuse.TypeTemplate(bool),
                    'keywords': confuse.StrSeq(),
                    'max_following': confuse.Integer(),
                    'multiple': confuse.TypeTemplate(bool)
                },
                'favorite': {
                    'enabled': confuse.TypeTemplate(bool),
                    'keywords': confuse.StrSeq()
                },
                'tag_friend': {
                    'enabled': confuse.TypeTemplate(bool),
                    'friends': confuse.StrSeq(),
                    'tag_keywords': confuse.StrSeq(),
                    'friend_keywords': confuse.StrSeq(),
                    'number_keywords': NumberKeywordsTemplate()
                }
            },

            'scheduler': {
                'search_interval': confuse.Integer(),
                'retweet_interval': confuse.Integer(),
                'retweet_random_margin': confuse.Integer(),
                'blocked_users_update_interval': confuse.Integer(),
                'clear_queue_interval': confuse.Integer(),
                'rate_limit_update_interval': confuse.Integer(),
                'check_mentions_interval': confuse.Integer(),
            },
        },
        'notifiers': {
            'mail': {
                'enabled': confuse.TypeTemplate(bool),
                'host': confuse.String(),
                'port': confuse.Integer(),
                'tls': confuse.TypeTemplate(bool),
                'username': confuse.String(),
                'password': confuse.String(),
                'recipient': confuse.String()
            },
            'pushbullet': {
                'enabled': confuse.TypeTemplate(bool),
                'token': confuse.String()
            }
        }
    }

    _valid = None

    @staticmethod
    def get():
        """
        Gets the static config object
        :return:
        """
        if Config._valid is None:
            raise ValueError("Configuration not loaded")
        return Config._valid

    @staticmethod
    def load(filename=None):
        """
        Loads a file and imports the settings
        :param filename: the file to import
        """
        config = confuse.LazyConfig('Yatcobot', __name__)

        # Add default config when in egg (using this way because egg is breaking the default way)
        if len(config.sources) == 0:
            default_config_text = pkg_resources.resource_string("yatcobot", "config_default.yaml")
            default_config = confuse.ConfigSource(yaml.load(default_config_text, Loader=confuse.Loader),
                                                  'pkg/config_default.yaml',
                                                  True)
            config.add(default_config)

        # Add user specified config
        if filename is not None and os.path.isfile(filename):
            config.set_file(filename)

        logger.info('Loading config files (From highest priority to lowest):')
        for i, config_source in enumerate(config.sources):
            logger.info('{}: Path: {}'.format(i, config_source.filename))
        Config._valid = config.get(Config.template)


class TwitterConfig(Config):

    @staticmethod
    def get():
        return super(TwitterConfig, TwitterConfig).get().twitter


class NotifiersConfig(Config):

    @staticmethod
    def get():
        return super(NotifiersConfig, NotifiersConfig).get().notifiers
