class Printable:
    """
    A mixin class that provides a default implementation for printable representations
    of objects. This class overrides the __repr__ and __str__ methods to return
    a string representation of all attributes of an instance.

    The mixin can be inherited by other classes to automatically equip them with
    readable string representations that include all instance variables.
    """

    def __repr__(self) -> str:
        """
        Provide the official string representation of the object, typically used for debugging.
        Returns a string in which each instance variable is represented as a key-value pair.

        Returns:
            str: A string representation of the object showing all instance variables.
        """
        return f'{self.__class__.__name__}({vars(self)})'

    def __str__(self) -> str:
        """
        Provide a nicely printable string representation of the object, meant for end-user output.
        Returns a string formatted similar to __repr__, but potentially less formal or detailed.

        Returns:
            str: A string representation of the object's instance variables.
        """
        return f'{self.__class__.__name__}({vars(self)})'
