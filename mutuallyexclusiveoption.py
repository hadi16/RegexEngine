from click import Option, UsageError


class MutuallyExclusiveOption(Option):
    """
    MutuallyExclusiveOption
    Class that inherits from click.Option superclass.
    Prevents the user from using multiple modes (regular, batch, etc.) simultaneously.

    Adapted from:
    https://stackoverflow.com/questions/37310718/
    mutually-exclusive-option-groups-in-python-click?noredirect=1&lq=1
    """

    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help_text = kwargs.get('help', '')
        if self.mutually_exclusive:
            ex_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = help_text + (
                    ' NOTE: This argument is mutually exclusive with  arguments: [' + ex_str + '].')
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError("Illegal usage: '{}' is mutually exclusive with '{}' options."
                             .format(self.name, ', '.join(self.mutually_exclusive)))
        return super(MutuallyExclusiveOption, self).handle_parse_result(ctx, opts, args)
