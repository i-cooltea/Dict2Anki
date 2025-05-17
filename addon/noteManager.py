from .constants import MODEL_FIELDS, BASIC_OPTION, EXTRA_OPTION
import logging

logger = logging.getLogger('dict2Anki.noteManager')
try:
    from aqt import mw
    import anki
except ImportError:
    from test.dummy_aqt import mw # type:ignore
    from test import dummy_anki as anki


def getDeckList():
    return [deck['name'] for deck in mw.col.decks.all()]


def getWordsByDeck(deckName) -> [str]:
    # notes = mw.col.findNotes(f'deck:"{deckName}"')
    notes = mw.col.find_notes(f'deck:"{deckName}"')
    words = []
    for nid in notes:
        # note = mw.col.getNote(nid)
        note = mw.col.get_note(nid)
        # if note.model().get('name', '').lower().startswith('dict2anki') and note['term']:
        if note.note_type().get('name', '').lower().startswith('dict2anki') and note['term']:

            words.append(note['term'])
    return words


def getNotes(wordList, deckName) -> list:
    notes = []
    for word in wordList:
        # note = mw.col.findNotes(f'deck:"{deckName}" term:"{word}"')
        note = mw.col.find_notes(f'deck:"{deckName}" term:"{word}"')
        if note:
            notes.append(note[0])
    return notes


def getOrCreateDeck(deckName, model):
    deck_id = mw.col.decks.id(deckName)
    deck = mw.col.decks.get(deck_id)
    mw.col.decks.select(deck['id'])
    mw.col.decks.save(deck)
    # mw.col.models.setCurrent(model)
    mw.col.models.set_current(model)
    model['did'] = deck['id']
    mw.col.models.save(model)
    mw.col.reset()
    mw.reset()
    return deck


def getOrCreateModel(modelName):
    # model = mw.col.models.byName(modelName)
    model = mw.col.models.by_name(modelName)
    if model:
        if set([f['name'] for f in model['flds']]) == set(MODEL_FIELDS):
            return model
        else:
            logger.warning('模版字段异常，自动删除重建')
            mw.col.models.rem(model)

    logger.info(f'创建新模版:{modelName}')
    newModel = mw.col.models.new(modelName)
    for field in MODEL_FIELDS:
        # mw.col.models.addField(newModel, mw.col.models.newField(field))
        mw.col.models.addField(newModel, mw.col.models.new_field(field))
    return newModel


def getOrCreateModelCardTemplate(modelObject, cardTemplateName):
    logger.info(f'添加卡片类型:{cardTemplateName}')
    existingCardTemplate = modelObject['tmpls']
    if cardTemplateName in [t.get('name') for t in existingCardTemplate]:
        return
    # cardTemplate = mw.col.models.newTemplate(cardTemplateName)
    cardTemplate = mw.col.models.new_template(cardTemplateName)
    cardTemplate['qfmt'] = '''
<div class="van-row van-row block block-word">
    <div role="separator" class="van-divider van-divider--hairline van-divider--content-center"
         style="margin: 5px 0px; font-size: 0.75em;">{{ 组 }}
    </div>
    <div class="van-collapse block__en">
        <div class="van-collapse-item">
            <div class="van-cell van-cell--clickable van-collapse-item__title" role="button" tabindex="0"
                 aria-expanded="false">
                <div class="van-cell__title">
                    <div class="van-row">
                        <div class="van-col van-col--3"></div>
                        <div class="van-col van-col--18">
                            <div id="txt-en" class="txt-en">{{ 英 }}</div>
                        </div>
                    </div>
                </div>
                <i
                        class="van-badge__wrapper van-icon van-icon-arrow van-cell__right-icon">
                </i></div>
        </div>
    </div>
    <div class="block__en txt-pron tappable" id="playBtn">
        <div class="van-row" style="text-align: center;">
            <div class="van-col van-col--4"></div>
            <div class="van-col van-col--16" style="padding-left: 15px;"><i
                    class="van-badge__wrapper van-icon van-icon-play-circle-o"></i> <span>{{ 音 }}</span></div>
        </div>
    </div>
</div>


<script>
var Http = new XMLHttpRequest();
var url='https://api.i-cooltea.top/v2/api/prepare?word={{英}}';
Http.open("HEAD", url);
Http.send();

</script>
    '''
    cardTemplate['afmt'] = '''
<div class="card-back">
    <div id="app"></div>
</div>
<script>
/* CreateBy Anki创享岛, 
 作者: 白日梦想家Ace 
 QQ群: 437107174
=================================
↓请在引号中输入您的激活码,可避免重复登录
================================*/
var accountNo="";
/* ==============================
↓请在引号中输入您的激活码,可避免重复登录
================================*/
 
 
var isBrowser = typeof window !== 'undefined';
var process = isBrowser ? {
env: {
  NODE_ENV: 'production'
}
} : require('process');
// define params
var appData = {
examType: "kaoyan",
word: {
  id: 0,
  cardId: `{{ID}}`,
  group: `{{组}}`,
  en: `{{英}}`,
  pron: "{{音}}",
  cn: `{{译2}}` || `{{译1}}`,
  note: `{{笔记}}`,
  tags: `{{Tags}}`
},
config:{
showSentenceCn: 1,
}
};

window.appData = appData;
// loading my app package
var script = document.createElement('script');
script.type = 'text/javascript';
script.src = 'https://ankix.i-cooltea.top/anki-word/prod/assets/main.js';
var head = document.getElementsByTagName('head')[0];
head.appendChild(script);

</script>
    '''
    modelObject['css'] = '''
@import url("https://ankix.i-cooltea.top/anki-word/prod/assets/style.css");
    '''
    mw.col.models.addTemplate(modelObject, cardTemplate)
    mw.col.models.add(modelObject)


def addNoteToDeck(deckObject, modelObject, currentConfig: dict, oneQueryResult: dict):
    if not oneQueryResult:
        logger.warning(f'查询结果{oneQueryResult} 异常，忽略')
        return
    modelObject['did'] = deckObject['id']

    newNote = anki.notes.Note(mw.col, modelObject)
    newNote['term'] = oneQueryResult['term']
    for configName in BASIC_OPTION + EXTRA_OPTION:
        logger.debug(f'字段:{configName}--结果:{oneQueryResult.get(configName)}')
        if oneQueryResult.get(configName):
            # 短语例句
            if configName in ['sentence', 'phrase'] and currentConfig[configName]:
                newNote[f'{configName}Front'] = '\n'.join(
                    [f'<tr><td>{e.strip()}</td></tr>' for e, _ in oneQueryResult[configName]])
                newNote[f'{configName}Back'] = '\n'.join(
                    [f'<tr><td>{e.strip()}<br>{c.strip()}</td></tr>' for e, c in oneQueryResult[configName]])
            # 图片
            elif configName == 'image':
                newNote[configName] = f'src="{oneQueryResult[configName]}"'
            # 释义
            elif configName == 'definition' and currentConfig[configName]:
                newNote[configName] = ' '.join(oneQueryResult[configName])
            # 发音
            elif configName in EXTRA_OPTION[:2]:
                newNote[configName] = f"[sound:{configName}_{oneQueryResult['term']}.mp3]"
            # 其他
            elif currentConfig[configName]:
                newNote[configName] = oneQueryResult[configName]

    mw.col.addNote(newNote)
    mw.col.reset()
    logger.info(f"添加笔记{newNote['term']}")
