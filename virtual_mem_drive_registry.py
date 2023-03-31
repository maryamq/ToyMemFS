# Global registry of all in-mem filesystems.
registry = {}


class VirtualMemDriveRegistry(type):
    """ Bare-bones registry system. This enables creating multiple virtual in-mem drives. 
        This enables multiple in-mem filesystems. 
        TODO(maryamq): Currently, there is no way to de-register a drive (P2).
    """
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        registry[obj.name] = obj
        print(f"Registered a new drive: {obj.name}")
        return obj
