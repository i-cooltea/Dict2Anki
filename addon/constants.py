VERSION = 'v6.1.6'
CUSTOM_BY_SHIGE = " (Develop for Anki创享岛 by Dream)"
RELEASE_URL = 'https://github.com/megachweng/Dict2Anki'
VERSION_CHECK_API = 'https://api.github.com/repos/megachweng/Dict2Anki/releases/latest'
MODEL_NAME = f'Dict2Anki-{VERSION}{CUSTOM_BY_SHIGE}'

BASIC_OPTION = ['definition', 'sentence', 'phrase', 'image', 'BrEPhonetic', 'AmEPhonetic']  # 顺序和名称不可修改
EXTRA_OPTION = ['BrEPron', 'AmEPron', 'noPron']  # 顺序和名称不可修改

MODEL_FIELDS = ['英', '音', '译1', '译2', '笔记']  # 名称不可修改