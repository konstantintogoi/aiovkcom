PERMISSIONS = (
    'notify',
    'friends',
    'photos',
    'audio',
    'video',
    'stories',
    'pages',
    'status',
    'notes',
    # 'messages',  # available only after moderation
    'wall',
    'offline',
    'docs',
    'groups',
    'notifications',
    'stats',
    'email',
    'market',
)

BITMASKS = {
    'notify': 1,
    'friends': 2,
    'photos': 4,
    'audio': 8,
    'video': 16,
    'stories': 64,
    'pages': 128,
    'status': 1024,
    'notes': 2048,
    'messages': 4096,
    'wall': 8192,
    'offline': 65536,
    'docs': 131072,
    'groups': 262144,
    'notifications': 524288,
    'stats': 1048576,
    'email': 4194304,
    'market': 134217728,
}


def bit_scope(permissions):
    return sum(BITMASKS[p] for p in permissions)
