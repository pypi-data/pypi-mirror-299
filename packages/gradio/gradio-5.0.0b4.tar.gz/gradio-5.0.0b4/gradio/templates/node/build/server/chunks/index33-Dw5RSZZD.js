import { C as ContextTracker, E as ExternalTokenizer, L as LRParser } from './index18-Bk6aUetb.js';
import { s as styleTags, t as tags, L as LRLanguage, i as indentNodeProp, f as foldNodeProp, u as bracketMatchingHandle, e as LanguageSupport, v as EditorView, h as syntaxTree, E as EditorSelection, p as parseMixed } from './Index19-Ct8qgVF0.js';
import { cssLanguage, css } from './index34-BoaxPsGz.js';
import { typescriptLanguage, jsxLanguage, tsxLanguage, javascriptLanguage, javascript } from './index35-DOFZZoSO.js';
import './ssr-Cz1f32Mr.js';
import './2-DpTvHskm.js';
import './index4-D_FyJKAV.js';
import './Download-BYY54H3I.js';
import './DownloadLink-4kzPen0P.js';
import './file-url-D-K40zdU.js';
import './Code-CNhFvcVb.js';
import './BlockLabel-DhtaXLPo.js';
import './Empty-DpvP4MVd.js';
import './Example10-DOFH6xbf.js';

const scriptText = 54, StartCloseScriptTag = 1, styleText = 55, StartCloseStyleTag = 2, textareaText = 56, StartCloseTextareaTag = 3, EndTag = 4, SelfClosingEndTag = 5, StartTag = 6, StartScriptTag = 7, StartStyleTag = 8, StartTextareaTag = 9, StartSelfClosingTag = 10, StartCloseTag = 11, NoMatchStartCloseTag = 12, MismatchedStartCloseTag = 13, missingCloseTag = 57, IncompleteCloseTag = 14, commentContent$1 = 58, Element = 20, TagName = 22, Attribute = 23, AttributeName = 24, AttributeValue = 26, UnquotedAttributeValue = 27, ScriptText = 28, StyleText = 31, TextareaText = 34, OpenTag = 36, CloseTag = 37, Dialect_noMatch = 0, Dialect_selfClosing = 1;
const selfClosers$1 = {
  area: true,
  base: true,
  br: true,
  col: true,
  command: true,
  embed: true,
  frame: true,
  hr: true,
  img: true,
  input: true,
  keygen: true,
  link: true,
  meta: true,
  param: true,
  source: true,
  track: true,
  wbr: true,
  menuitem: true
};
const implicitlyClosed = {
  dd: true,
  li: true,
  optgroup: true,
  option: true,
  p: true,
  rp: true,
  rt: true,
  tbody: true,
  td: true,
  tfoot: true,
  th: true,
  tr: true
};
const closeOnOpen = {
  dd: { dd: true, dt: true },
  dt: { dd: true, dt: true },
  li: { li: true },
  option: { option: true, optgroup: true },
  optgroup: { optgroup: true },
  p: {
    address: true,
    article: true,
    aside: true,
    blockquote: true,
    dir: true,
    div: true,
    dl: true,
    fieldset: true,
    footer: true,
    form: true,
    h1: true,
    h2: true,
    h3: true,
    h4: true,
    h5: true,
    h6: true,
    header: true,
    hgroup: true,
    hr: true,
    menu: true,
    nav: true,
    ol: true,
    p: true,
    pre: true,
    section: true,
    table: true,
    ul: true
  },
  rp: { rp: true, rt: true },
  rt: { rp: true, rt: true },
  tbody: { tbody: true, tfoot: true },
  td: { td: true, th: true },
  tfoot: { tbody: true },
  th: { td: true, th: true },
  thead: { tbody: true, tfoot: true },
  tr: { tr: true }
};
function nameChar(ch) {
  return ch == 45 || ch == 46 || ch == 58 || ch >= 65 && ch <= 90 || ch == 95 || ch >= 97 && ch <= 122 || ch >= 161;
}
function isSpace(ch) {
  return ch == 9 || ch == 10 || ch == 13 || ch == 32;
}
let cachedName = null, cachedInput = null, cachedPos = 0;
function tagNameAfter(input, offset) {
  let pos = input.pos + offset;
  if (cachedPos == pos && cachedInput == input)
    return cachedName;
  let next = input.peek(offset);
  while (isSpace(next))
    next = input.peek(++offset);
  let name = "";
  for (; ; ) {
    if (!nameChar(next))
      break;
    name += String.fromCharCode(next);
    next = input.peek(++offset);
  }
  cachedInput = input;
  cachedPos = pos;
  return cachedName = name ? name.toLowerCase() : next == question || next == bang ? void 0 : null;
}
const lessThan = 60, greaterThan = 62, slash = 47, question = 63, bang = 33, dash = 45;
function ElementContext(name, parent) {
  this.name = name;
  this.parent = parent;
  this.hash = parent ? parent.hash : 0;
  for (let i = 0; i < name.length; i++)
    this.hash += (this.hash << 4) + name.charCodeAt(i) + (name.charCodeAt(i) << 8);
}
const startTagTerms = [StartTag, StartSelfClosingTag, StartScriptTag, StartStyleTag, StartTextareaTag];
const elementContext = new ContextTracker({
  start: null,
  shift(context, term, stack, input) {
    return startTagTerms.indexOf(term) > -1 ? new ElementContext(tagNameAfter(input, 1) || "", context) : context;
  },
  reduce(context, term) {
    return term == Element && context ? context.parent : context;
  },
  reuse(context, node, stack, input) {
    let type = node.type.id;
    return type == StartTag || type == OpenTag ? new ElementContext(tagNameAfter(input, 1) || "", context) : context;
  },
  hash(context) {
    return context ? context.hash : 0;
  },
  strict: false
});
const tagStart = new ExternalTokenizer((input, stack) => {
  if (input.next != lessThan) {
    if (input.next < 0 && stack.context)
      input.acceptToken(missingCloseTag);
    return;
  }
  input.advance();
  let close = input.next == slash;
  if (close)
    input.advance();
  let name = tagNameAfter(input, 0);
  if (name === void 0)
    return;
  if (!name)
    return input.acceptToken(close ? IncompleteCloseTag : StartTag);
  let parent = stack.context ? stack.context.name : null;
  if (close) {
    if (name == parent)
      return input.acceptToken(StartCloseTag);
    if (parent && implicitlyClosed[parent])
      return input.acceptToken(missingCloseTag, -2);
    if (stack.dialectEnabled(Dialect_noMatch))
      return input.acceptToken(NoMatchStartCloseTag);
    for (let cx = stack.context; cx; cx = cx.parent)
      if (cx.name == name)
        return;
    input.acceptToken(MismatchedStartCloseTag);
  } else {
    if (name == "script")
      return input.acceptToken(StartScriptTag);
    if (name == "style")
      return input.acceptToken(StartStyleTag);
    if (name == "textarea")
      return input.acceptToken(StartTextareaTag);
    if (selfClosers$1.hasOwnProperty(name))
      return input.acceptToken(StartSelfClosingTag);
    if (parent && closeOnOpen[parent] && closeOnOpen[parent][name])
      input.acceptToken(missingCloseTag, -1);
    else
      input.acceptToken(StartTag);
  }
}, { contextual: true });
const commentContent = new ExternalTokenizer((input) => {
  for (let dashes = 0, i = 0; ; i++) {
    if (input.next < 0) {
      if (i)
        input.acceptToken(commentContent$1);
      break;
    }
    if (input.next == dash) {
      dashes++;
    } else if (input.next == greaterThan && dashes >= 2) {
      if (i > 3)
        input.acceptToken(commentContent$1, -2);
      break;
    } else {
      dashes = 0;
    }
    input.advance();
  }
});
function inForeignElement(context) {
  for (; context; context = context.parent)
    if (context.name == "svg" || context.name == "math")
      return true;
  return false;
}
const endTag = new ExternalTokenizer((input, stack) => {
  if (input.next == slash && input.peek(1) == greaterThan) {
    let selfClosing = stack.dialectEnabled(Dialect_selfClosing) || inForeignElement(stack.context);
    input.acceptToken(selfClosing ? SelfClosingEndTag : EndTag, 2);
  } else if (input.next == greaterThan) {
    input.acceptToken(EndTag, 1);
  }
});
function contentTokenizer(tag, textToken, endToken) {
  let lastState = 2 + tag.length;
  return new ExternalTokenizer((input) => {
    for (let state = 0, matchedLen = 0, i = 0; ; i++) {
      if (input.next < 0) {
        if (i)
          input.acceptToken(textToken);
        break;
      }
      if (state == 0 && input.next == lessThan || state == 1 && input.next == slash || state >= 2 && state < lastState && input.next == tag.charCodeAt(state - 2)) {
        state++;
        matchedLen++;
      } else if ((state == 2 || state == lastState) && isSpace(input.next)) {
        matchedLen++;
      } else if (state == lastState && input.next == greaterThan) {
        if (i > matchedLen)
          input.acceptToken(textToken, -matchedLen);
        else
          input.acceptToken(endToken, -(matchedLen - 2));
        break;
      } else if ((input.next == 10 || input.next == 13) && i) {
        input.acceptToken(textToken, 1);
        break;
      } else {
        state = matchedLen = 0;
      }
      input.advance();
    }
  });
}
const scriptTokens = contentTokenizer("script", scriptText, StartCloseScriptTag);
const styleTokens = contentTokenizer("style", styleText, StartCloseStyleTag);
const textareaTokens = contentTokenizer("textarea", textareaText, StartCloseTextareaTag);
const htmlHighlighting = styleTags({
  "Text RawText": tags.content,
  "StartTag StartCloseTag SelfClosingEndTag EndTag": tags.angleBracket,
  TagName: tags.tagName,
  "MismatchedCloseTag/TagName": [tags.tagName, tags.invalid],
  AttributeName: tags.attributeName,
  "AttributeValue UnquotedAttributeValue": tags.attributeValue,
  Is: tags.definitionOperator,
  "EntityReference CharacterReference": tags.character,
  Comment: tags.blockComment,
  ProcessingInst: tags.processingInstruction,
  DoctypeDecl: tags.documentMeta
});
const parser = LRParser.deserialize({
  version: 14,
  states: ",xOVO!rOOO!WQ#tO'#CqO!]Q#tO'#CzO!bQ#tO'#C}O!gQ#tO'#DQO!lQ#tO'#DSO!qOaO'#CpO!|ObO'#CpO#XOdO'#CpO$eO!rO'#CpOOO`'#Cp'#CpO$lO$fO'#DTO$tQ#tO'#DVO$yQ#tO'#DWOOO`'#Dk'#DkOOO`'#DY'#DYQVO!rOOO%OQ&rO,59]O%WQ&rO,59fO%`Q&rO,59iO%hQ&rO,59lO%sQ&rO,59nOOOa'#D^'#D^O%{OaO'#CxO&WOaO,59[OOOb'#D_'#D_O&`ObO'#C{O&kObO,59[OOOd'#D`'#D`O&sOdO'#DOO'OOdO,59[OOO`'#Da'#DaO'WO!rO,59[O'_Q#tO'#DROOO`,59[,59[OOOp'#Db'#DbO'dO$fO,59oOOO`,59o,59oO'lQ#|O,59qO'qQ#|O,59rOOO`-E7W-E7WO'vQ&rO'#CsOOQW'#DZ'#DZO(UQ&rO1G.wOOOa1G.w1G.wO(^Q&rO1G/QOOOb1G/Q1G/QO(fQ&rO1G/TOOOd1G/T1G/TO(nQ&rO1G/WOOO`1G/W1G/WOOO`1G/Y1G/YO(yQ&rO1G/YOOOa-E7[-E7[O)RQ#tO'#CyOOO`1G.v1G.vOOOb-E7]-E7]O)WQ#tO'#C|OOOd-E7^-E7^O)]Q#tO'#DPOOO`-E7_-E7_O)bQ#|O,59mOOOp-E7`-E7`OOO`1G/Z1G/ZOOO`1G/]1G/]OOO`1G/^1G/^O)gQ,UO,59_OOQW-E7X-E7XOOOa7+$c7+$cOOOb7+$l7+$lOOOd7+$o7+$oOOO`7+$r7+$rOOO`7+$t7+$tO)rQ#|O,59eO)wQ#|O,59hO)|Q#|O,59kOOO`1G/X1G/XO*RO7[O'#CvO*dOMhO'#CvOOQW1G.y1G.yOOO`1G/P1G/POOO`1G/S1G/SOOO`1G/V1G/VOOOO'#D['#D[O*uO7[O,59bOOQW,59b,59bOOOO'#D]'#D]O+WOMhO,59bOOOO-E7Y-E7YOOQW1G.|1G.|OOOO-E7Z-E7Z",
  stateData: "+s~O!^OS~OUSOVPOWQOXROYTO[]O][O^^O`^Oa^Ob^Oc^Ox^O{_O!dZO~OfaO~OfbO~OfcO~OfdO~OfeO~O!WfOPlP!ZlP~O!XiOQoP!ZoP~O!YlORrP!ZrP~OUSOVPOWQOXROYTOZqO[]O][O^^O`^Oa^Ob^Oc^Ox^O!dZO~O!ZrO~P#dO![sO!euO~OfvO~OfwO~OS|OhyO~OS!OOhyO~OS!QOhyO~OS!SOT!TOhyO~OS!TOhyO~O!WfOPlX!ZlX~OP!WO!Z!XO~O!XiOQoX!ZoX~OQ!ZO!Z!XO~O!YlORrX!ZrX~OR!]O!Z!XO~O!Z!XO~P#dOf!_O~O![sO!e!aO~OS!bO~OS!cO~Oi!dOSgXhgXTgX~OS!fOhyO~OS!gOhyO~OS!hOhyO~OS!iOT!jOhyO~OS!jOhyO~Of!kO~Of!lO~Of!mO~OS!nO~Ok!qO!`!oO!b!pO~OS!rO~OS!sO~OS!tO~Oa!uOb!uOc!uO!`!wO!a!uO~Oa!xOb!xOc!xO!b!wO!c!xO~Oa!uOb!uOc!uO!`!{O!a!uO~Oa!xOb!xOc!xO!b!{O!c!xO~OT~bac!dx{!d~",
  goto: "%p!`PPPPPPPPPPPPPPPPPPPP!a!gP!mPP!yP!|#P#S#Y#]#`#f#i#l#r#x!aP!a!aP$O$U$l$r$x%O%U%[%bPPPPPPPP%hX^OX`pXUOX`pezabcde{}!P!R!UR!q!dRhUR!XhXVOX`pRkVR!XkXWOX`pRnWR!XnXXOX`pQrXR!XpXYOX`pQ`ORx`Q{aQ}bQ!PcQ!RdQ!UeZ!e{}!P!R!UQ!v!oR!z!vQ!y!pR!|!yQgUR!VgQjVR!YjQmWR![mQpXR!^pQtZR!`tS_O`ToXp",
  nodeNames: "⚠ StartCloseTag StartCloseTag StartCloseTag EndTag SelfClosingEndTag StartTag StartTag StartTag StartTag StartTag StartCloseTag StartCloseTag StartCloseTag IncompleteCloseTag Document Text EntityReference CharacterReference InvalidEntity Element OpenTag TagName Attribute AttributeName Is AttributeValue UnquotedAttributeValue ScriptText CloseTag OpenTag StyleText CloseTag OpenTag TextareaText CloseTag OpenTag CloseTag SelfClosingTag Comment ProcessingInst MismatchedCloseTag CloseTag DoctypeDecl",
  maxTerm: 67,
  context: elementContext,
  nodeProps: [
    ["closedBy", -10, 1, 2, 3, 7, 8, 9, 10, 11, 12, 13, "EndTag", 6, "EndTag SelfClosingEndTag", -4, 21, 30, 33, 36, "CloseTag"],
    ["openedBy", 4, "StartTag StartCloseTag", 5, "StartTag", -4, 29, 32, 35, 37, "OpenTag"],
    ["group", -9, 14, 17, 18, 19, 20, 39, 40, 41, 42, "Entity", 16, "Entity TextContent", -3, 28, 31, 34, "TextContent Entity"]
  ],
  propSources: [htmlHighlighting],
  skippedNodes: [0],
  repeatNodeCount: 9,
  tokenData: "!<p!aR!YOX$qXY,QYZ,QZ[$q[]&X]^,Q^p$qpq,Qqr-_rs3_sv-_vw3}wxHYx}-_}!OH{!O!P-_!P!Q$q!Q![-_![!]Mz!]!^-_!^!_!$S!_!`!;x!`!a&X!a!c-_!c!}Mz!}#R-_#R#SMz#S#T1k#T#oMz#o#s-_#s$f$q$f%W-_%W%oMz%o%p-_%p&aMz&a&b-_&b1pMz1p4U-_4U4dMz4d4e-_4e$ISMz$IS$I`-_$I`$IbMz$Ib$Kh-_$Kh%#tMz%#t&/x-_&/x&EtMz&Et&FV-_&FV;'SMz;'S;:j!#|;:j;=`3X<%l?&r-_?&r?AhMz?Ah?BY$q?BY?MnMz?MnO$q!Z$|c`PkW!a`!cpOX$qXZ&XZ[$q[^&X^p$qpq&Xqr$qrs&}sv$qvw+Pwx(tx!^$q!^!_*V!_!a&X!a#S$q#S#T&X#T;'S$q;'S;=`+z<%lO$q!R&bX`P!a`!cpOr&Xrs&}sv&Xwx(tx!^&X!^!_*V!_;'S&X;'S;=`*y<%lO&Xq'UV`P!cpOv&}wx'kx!^&}!^!_(V!_;'S&};'S;=`(n<%lO&}P'pT`POv'kw!^'k!_;'S'k;'S;=`(P<%lO'kP(SP;=`<%l'kp([S!cpOv(Vx;'S(V;'S;=`(h<%lO(Vp(kP;=`<%l(Vq(qP;=`<%l&}a({W`P!a`Or(trs'ksv(tw!^(t!^!_)e!_;'S(t;'S;=`*P<%lO(t`)jT!a`Or)esv)ew;'S)e;'S;=`)y<%lO)e`)|P;=`<%l)ea*SP;=`<%l(t!Q*^V!a`!cpOr*Vrs(Vsv*Vwx)ex;'S*V;'S;=`*s<%lO*V!Q*vP;=`<%l*V!R*|P;=`<%l&XW+UYkWOX+PZ[+P^p+Pqr+Psw+Px!^+P!a#S+P#T;'S+P;'S;=`+t<%lO+PW+wP;=`<%l+P!Z+}P;=`<%l$q!a,]``P!a`!cp!^^OX&XXY,QYZ,QZ]&X]^,Q^p&Xpq,Qqr&Xrs&}sv&Xwx(tx!^&X!^!_*V!_;'S&X;'S;=`*y<%lO&X!_-ljhS`PkW!a`!cpOX$qXZ&XZ[$q[^&X^p$qpq&Xqr-_rs&}sv-_vw/^wx(tx!P-_!P!Q$q!Q!^-_!^!_*V!_!a&X!a#S-_#S#T1k#T#s-_#s$f$q$f;'S-_;'S;=`3X<%l?Ah-_?Ah?BY$q?BY?Mn-_?MnO$q[/ebhSkWOX+PZ[+P^p+Pqr/^sw/^x!P/^!P!Q+P!Q!^/^!a#S/^#S#T0m#T#s/^#s$f+P$f;'S/^;'S;=`1e<%l?Ah/^?Ah?BY+P?BY?Mn/^?MnO+PS0rXhSqr0msw0mx!P0m!Q!^0m!a#s0m$f;'S0m;'S;=`1_<%l?Ah0m?BY?Mn0mS1bP;=`<%l0m[1hP;=`<%l/^!V1vchS`P!a`!cpOq&Xqr1krs&}sv1kvw0mwx(tx!P1k!P!Q&X!Q!^1k!^!_*V!_!a&X!a#s1k#s$f&X$f;'S1k;'S;=`3R<%l?Ah1k?Ah?BY&X?BY?Mn1k?MnO&X!V3UP;=`<%l1k!_3[P;=`<%l-_!Z3hV!`h`P!cpOv&}wx'kx!^&}!^!_(V!_;'S&};'S;=`(n<%lO&}!_4WihSkWc!ROX5uXZ7SZ[5u[^7S^p5uqr8trs7Sst>]tw8twx7Sx!P8t!P!Q5u!Q!]8t!]!^/^!^!a7S!a#S8t#S#T;{#T#s8t#s$f5u$f;'S8t;'S;=`>V<%l?Ah8t?Ah?BY5u?BY?Mn8t?MnO5u!Z5zbkWOX5uXZ7SZ[5u[^7S^p5uqr5urs7Sst+Ptw5uwx7Sx!]5u!]!^7w!^!a7S!a#S5u#S#T7S#T;'S5u;'S;=`8n<%lO5u!R7VVOp7Sqs7St!]7S!]!^7l!^;'S7S;'S;=`7q<%lO7S!R7qOa!R!R7tP;=`<%l7S!Z8OYkWa!ROX+PZ[+P^p+Pqr+Psw+Px!^+P!a#S+P#T;'S+P;'S;=`+t<%lO+P!Z8qP;=`<%l5u!_8{ihSkWOX5uXZ7SZ[5u[^7S^p5uqr8trs7Sst/^tw8twx7Sx!P8t!P!Q5u!Q!]8t!]!^:j!^!a7S!a#S8t#S#T;{#T#s8t#s$f5u$f;'S8t;'S;=`>V<%l?Ah8t?Ah?BY5u?BY?Mn8t?MnO5u!_:sbhSkWa!ROX+PZ[+P^p+Pqr/^sw/^x!P/^!P!Q+P!Q!^/^!a#S/^#S#T0m#T#s/^#s$f+P$f;'S/^;'S;=`1e<%l?Ah/^?Ah?BY+P?BY?Mn/^?MnO+P!V<QchSOp7Sqr;{rs7Sst0mtw;{wx7Sx!P;{!P!Q7S!Q!];{!]!^=]!^!a7S!a#s;{#s$f7S$f;'S;{;'S;=`>P<%l?Ah;{?Ah?BY7S?BY?Mn;{?MnO7S!V=dXhSa!Rqr0msw0mx!P0m!Q!^0m!a#s0m$f;'S0m;'S;=`1_<%l?Ah0m?BY?Mn0m!V>SP;=`<%l;{!_>YP;=`<%l8t!_>dhhSkWOX@OXZAYZ[@O[^AY^p@OqrBwrsAYswBwwxAYx!PBw!P!Q@O!Q!]Bw!]!^/^!^!aAY!a#SBw#S#TE{#T#sBw#s$f@O$f;'SBw;'S;=`HS<%l?AhBw?Ah?BY@O?BY?MnBw?MnO@O!Z@TakWOX@OXZAYZ[@O[^AY^p@Oqr@OrsAYsw@OwxAYx!]@O!]!^Az!^!aAY!a#S@O#S#TAY#T;'S@O;'S;=`Bq<%lO@O!RA]UOpAYq!]AY!]!^Ao!^;'SAY;'S;=`At<%lOAY!RAtOb!R!RAwP;=`<%lAY!ZBRYkWb!ROX+PZ[+P^p+Pqr+Psw+Px!^+P!a#S+P#T;'S+P;'S;=`+t<%lO+P!ZBtP;=`<%l@O!_COhhSkWOX@OXZAYZ[@O[^AY^p@OqrBwrsAYswBwwxAYx!PBw!P!Q@O!Q!]Bw!]!^Dj!^!aAY!a#SBw#S#TE{#T#sBw#s$f@O$f;'SBw;'S;=`HS<%l?AhBw?Ah?BY@O?BY?MnBw?MnO@O!_DsbhSkWb!ROX+PZ[+P^p+Pqr/^sw/^x!P/^!P!Q+P!Q!^/^!a#S/^#S#T0m#T#s/^#s$f+P$f;'S/^;'S;=`1e<%l?Ah/^?Ah?BY+P?BY?Mn/^?MnO+P!VFQbhSOpAYqrE{rsAYswE{wxAYx!PE{!P!QAY!Q!]E{!]!^GY!^!aAY!a#sE{#s$fAY$f;'SE{;'S;=`G|<%l?AhE{?Ah?BYAY?BY?MnE{?MnOAY!VGaXhSb!Rqr0msw0mx!P0m!Q!^0m!a#s0m$f;'S0m;'S;=`1_<%l?Ah0m?BY?Mn0m!VHPP;=`<%lE{!_HVP;=`<%lBw!ZHcW!bx`P!a`Or(trs'ksv(tw!^(t!^!_)e!_;'S(t;'S;=`*P<%lO(t!aIYlhS`PkW!a`!cpOX$qXZ&XZ[$q[^&X^p$qpq&Xqr-_rs&}sv-_vw/^wx(tx}-_}!OKQ!O!P-_!P!Q$q!Q!^-_!^!_*V!_!a&X!a#S-_#S#T1k#T#s-_#s$f$q$f;'S-_;'S;=`3X<%l?Ah-_?Ah?BY$q?BY?Mn-_?MnO$q!aK_khS`PkW!a`!cpOX$qXZ&XZ[$q[^&X^p$qpq&Xqr-_rs&}sv-_vw/^wx(tx!P-_!P!Q$q!Q!^-_!^!_*V!_!`&X!`!aMS!a#S-_#S#T1k#T#s-_#s$f$q$f;'S-_;'S;=`3X<%l?Ah-_?Ah?BY$q?BY?Mn-_?MnO$q!TM_X`P!a`!cp!eQOr&Xrs&}sv&Xwx(tx!^&X!^!_*V!_;'S&X;'S;=`*y<%lO&X!aNZ!ZhSfQ`PkW!a`!cpOX$qXZ&XZ[$q[^&X^p$qpq&Xqr-_rs&}sv-_vw/^wx(tx}-_}!OMz!O!PMz!P!Q$q!Q![Mz![!]Mz!]!^-_!^!_*V!_!a&X!a!c-_!c!}Mz!}#R-_#R#SMz#S#T1k#T#oMz#o#s-_#s$f$q$f$}-_$}%OMz%O%W-_%W%oMz%o%p-_%p&aMz&a&b-_&b1pMz1p4UMz4U4dMz4d4e-_4e$ISMz$IS$I`-_$I`$IbMz$Ib$Je-_$Je$JgMz$Jg$Kh-_$Kh%#tMz%#t&/x-_&/x&EtMz&Et&FV-_&FV;'SMz;'S;:j!#|;:j;=`3X<%l?&r-_?&r?AhMz?Ah?BY$q?BY?MnMz?MnO$q!a!$PP;=`<%lMz!R!$ZY!a`!cpOq*Vqr!$yrs(Vsv*Vwx)ex!a*V!a!b!4t!b;'S*V;'S;=`*s<%lO*V!R!%Q]!a`!cpOr*Vrs(Vsv*Vwx)ex}*V}!O!%y!O!f*V!f!g!']!g#W*V#W#X!0`#X;'S*V;'S;=`*s<%lO*V!R!&QX!a`!cpOr*Vrs(Vsv*Vwx)ex}*V}!O!&m!O;'S*V;'S;=`*s<%lO*V!R!&vV!a`!cp!dPOr*Vrs(Vsv*Vwx)ex;'S*V;'S;=`*s<%lO*V!R!'dX!a`!cpOr*Vrs(Vsv*Vwx)ex!q*V!q!r!(P!r;'S*V;'S;=`*s<%lO*V!R!(WX!a`!cpOr*Vrs(Vsv*Vwx)ex!e*V!e!f!(s!f;'S*V;'S;=`*s<%lO*V!R!(zX!a`!cpOr*Vrs(Vsv*Vwx)ex!v*V!v!w!)g!w;'S*V;'S;=`*s<%lO*V!R!)nX!a`!cpOr*Vrs(Vsv*Vwx)ex!{*V!{!|!*Z!|;'S*V;'S;=`*s<%lO*V!R!*bX!a`!cpOr*Vrs(Vsv*Vwx)ex!r*V!r!s!*}!s;'S*V;'S;=`*s<%lO*V!R!+UX!a`!cpOr*Vrs(Vsv*Vwx)ex!g*V!g!h!+q!h;'S*V;'S;=`*s<%lO*V!R!+xY!a`!cpOr!+qrs!,hsv!+qvw!-Swx!.[x!`!+q!`!a!/j!a;'S!+q;'S;=`!0Y<%lO!+qq!,mV!cpOv!,hvx!-Sx!`!,h!`!a!-q!a;'S!,h;'S;=`!.U<%lO!,hP!-VTO!`!-S!`!a!-f!a;'S!-S;'S;=`!-k<%lO!-SP!-kO{PP!-nP;=`<%l!-Sq!-xS!cp{POv(Vx;'S(V;'S;=`(h<%lO(Vq!.XP;=`<%l!,ha!.aX!a`Or!.[rs!-Ssv!.[vw!-Sw!`!.[!`!a!.|!a;'S!.[;'S;=`!/d<%lO!.[a!/TT!a`{POr)esv)ew;'S)e;'S;=`)y<%lO)ea!/gP;=`<%l!.[!R!/sV!a`!cp{POr*Vrs(Vsv*Vwx)ex;'S*V;'S;=`*s<%lO*V!R!0]P;=`<%l!+q!R!0gX!a`!cpOr*Vrs(Vsv*Vwx)ex#c*V#c#d!1S#d;'S*V;'S;=`*s<%lO*V!R!1ZX!a`!cpOr*Vrs(Vsv*Vwx)ex#V*V#V#W!1v#W;'S*V;'S;=`*s<%lO*V!R!1}X!a`!cpOr*Vrs(Vsv*Vwx)ex#h*V#h#i!2j#i;'S*V;'S;=`*s<%lO*V!R!2qX!a`!cpOr*Vrs(Vsv*Vwx)ex#m*V#m#n!3^#n;'S*V;'S;=`*s<%lO*V!R!3eX!a`!cpOr*Vrs(Vsv*Vwx)ex#d*V#d#e!4Q#e;'S*V;'S;=`*s<%lO*V!R!4XX!a`!cpOr*Vrs(Vsv*Vwx)ex#X*V#X#Y!+q#Y;'S*V;'S;=`*s<%lO*V!R!4{Y!a`!cpOr!4trs!5ksv!4tvw!6Vwx!8]x!a!4t!a!b!:]!b;'S!4t;'S;=`!;r<%lO!4tq!5pV!cpOv!5kvx!6Vx!a!5k!a!b!7W!b;'S!5k;'S;=`!8V<%lO!5kP!6YTO!a!6V!a!b!6i!b;'S!6V;'S;=`!7Q<%lO!6VP!6lTO!`!6V!`!a!6{!a;'S!6V;'S;=`!7Q<%lO!6VP!7QOxPP!7TP;=`<%l!6Vq!7]V!cpOv!5kvx!6Vx!`!5k!`!a!7r!a;'S!5k;'S;=`!8V<%lO!5kq!7yS!cpxPOv(Vx;'S(V;'S;=`(h<%lO(Vq!8YP;=`<%l!5ka!8bX!a`Or!8]rs!6Vsv!8]vw!6Vw!a!8]!a!b!8}!b;'S!8];'S;=`!:V<%lO!8]a!9SX!a`Or!8]rs!6Vsv!8]vw!6Vw!`!8]!`!a!9o!a;'S!8];'S;=`!:V<%lO!8]a!9vT!a`xPOr)esv)ew;'S)e;'S;=`)y<%lO)ea!:YP;=`<%l!8]!R!:dY!a`!cpOr!4trs!5ksv!4tvw!6Vwx!8]x!`!4t!`!a!;S!a;'S!4t;'S;=`!;r<%lO!4t!R!;]V!a`!cpxPOr*Vrs(Vsv*Vwx)ex;'S*V;'S;=`*s<%lO*V!R!;uP;=`<%l!4t!V!<TXiS`P!a`!cpOr&Xrs&}sv&Xwx(tx!^&X!^!_*V!_;'S&X;'S;=`*y<%lO&X",
  tokenizers: [scriptTokens, styleTokens, textareaTokens, endTag, tagStart, commentContent, 0, 1, 2, 3, 4, 5],
  topRules: { "Document": [0, 15] },
  dialects: { noMatch: 0, selfClosing: 485 },
  tokenPrec: 487
});
function getAttrs(openTag, input) {
  let attrs = /* @__PURE__ */ Object.create(null);
  for (let att of openTag.getChildren(Attribute)) {
    let name = att.getChild(AttributeName), value = att.getChild(AttributeValue) || att.getChild(UnquotedAttributeValue);
    if (name)
      attrs[input.read(name.from, name.to)] = !value ? "" : value.type.id == AttributeValue ? input.read(value.from + 1, value.to - 1) : input.read(value.from, value.to);
  }
  return attrs;
}
function findTagName(openTag, input) {
  let tagNameNode = openTag.getChild(TagName);
  return tagNameNode ? input.read(tagNameNode.from, tagNameNode.to) : " ";
}
function maybeNest(node, input, tags2) {
  let attrs;
  for (let tag of tags2) {
    if (!tag.attrs || tag.attrs(attrs || (attrs = getAttrs(node.node.parent.firstChild, input))))
      return { parser: tag.parser };
  }
  return null;
}
function configureNesting(tags2 = [], attributes = []) {
  let script = [], style = [], textarea = [], other = [];
  for (let tag of tags2) {
    let array = tag.tag == "script" ? script : tag.tag == "style" ? style : tag.tag == "textarea" ? textarea : other;
    array.push(tag);
  }
  let attrs = attributes.length ? /* @__PURE__ */ Object.create(null) : null;
  for (let attr of attributes)
    (attrs[attr.name] || (attrs[attr.name] = [])).push(attr);
  return parseMixed((node, input) => {
    let id = node.type.id;
    if (id == ScriptText)
      return maybeNest(node, input, script);
    if (id == StyleText)
      return maybeNest(node, input, style);
    if (id == TextareaText)
      return maybeNest(node, input, textarea);
    if (id == Element && other.length) {
      let n = node.node, open = n.firstChild, tagName = open && findTagName(open, input), attrs2;
      if (tagName)
        for (let tag of other) {
          if (tag.tag == tagName && (!tag.attrs || tag.attrs(attrs2 || (attrs2 = getAttrs(n, input))))) {
            let close = n.lastChild;
            return { parser: tag.parser, overlay: [{ from: open.to, to: close.type.id == CloseTag ? close.from : n.to }] };
          }
        }
    }
    if (attrs && id == Attribute) {
      let n = node.node, nameNode;
      if (nameNode = n.firstChild) {
        let matches = attrs[input.read(nameNode.from, nameNode.to)];
        if (matches)
          for (let attr of matches) {
            if (attr.tagName && attr.tagName != findTagName(n.parent, input))
              continue;
            let value = n.lastChild;
            if (value.type.id == AttributeValue) {
              let from = value.from + 1;
              let last = value.lastChild, to = value.to - (last && last.isError ? 0 : 1);
              if (to > from)
                return { parser: attr.parser, overlay: [{ from, to }] };
            } else if (value.type.id == UnquotedAttributeValue) {
              return { parser: attr.parser, overlay: [{ from: value.from, to: value.to }] };
            }
          }
      }
    }
    return null;
  });
}
const Targets = ["_blank", "_self", "_top", "_parent"];
const Charsets = ["ascii", "utf-8", "utf-16", "latin1", "latin1"];
const Methods = ["get", "post", "put", "delete"];
const Encs = ["application/x-www-form-urlencoded", "multipart/form-data", "text/plain"];
const Bool = ["true", "false"];
const S = {};
const Tags = {
  a: {
    attrs: {
      href: null,
      ping: null,
      type: null,
      media: null,
      target: Targets,
      hreflang: null
    }
  },
  abbr: S,
  address: S,
  area: {
    attrs: {
      alt: null,
      coords: null,
      href: null,
      target: null,
      ping: null,
      media: null,
      hreflang: null,
      type: null,
      shape: ["default", "rect", "circle", "poly"]
    }
  },
  article: S,
  aside: S,
  audio: {
    attrs: {
      src: null,
      mediagroup: null,
      crossorigin: ["anonymous", "use-credentials"],
      preload: ["none", "metadata", "auto"],
      autoplay: ["autoplay"],
      loop: ["loop"],
      controls: ["controls"]
    }
  },
  b: S,
  base: { attrs: { href: null, target: Targets } },
  bdi: S,
  bdo: S,
  blockquote: { attrs: { cite: null } },
  body: S,
  br: S,
  button: {
    attrs: {
      form: null,
      formaction: null,
      name: null,
      value: null,
      autofocus: ["autofocus"],
      disabled: ["autofocus"],
      formenctype: Encs,
      formmethod: Methods,
      formnovalidate: ["novalidate"],
      formtarget: Targets,
      type: ["submit", "reset", "button"]
    }
  },
  canvas: { attrs: { width: null, height: null } },
  caption: S,
  center: S,
  cite: S,
  code: S,
  col: { attrs: { span: null } },
  colgroup: { attrs: { span: null } },
  command: {
    attrs: {
      type: ["command", "checkbox", "radio"],
      label: null,
      icon: null,
      radiogroup: null,
      command: null,
      title: null,
      disabled: ["disabled"],
      checked: ["checked"]
    }
  },
  data: { attrs: { value: null } },
  datagrid: { attrs: { disabled: ["disabled"], multiple: ["multiple"] } },
  datalist: { attrs: { data: null } },
  dd: S,
  del: { attrs: { cite: null, datetime: null } },
  details: { attrs: { open: ["open"] } },
  dfn: S,
  div: S,
  dl: S,
  dt: S,
  em: S,
  embed: { attrs: { src: null, type: null, width: null, height: null } },
  eventsource: { attrs: { src: null } },
  fieldset: { attrs: { disabled: ["disabled"], form: null, name: null } },
  figcaption: S,
  figure: S,
  footer: S,
  form: {
    attrs: {
      action: null,
      name: null,
      "accept-charset": Charsets,
      autocomplete: ["on", "off"],
      enctype: Encs,
      method: Methods,
      novalidate: ["novalidate"],
      target: Targets
    }
  },
  h1: S,
  h2: S,
  h3: S,
  h4: S,
  h5: S,
  h6: S,
  head: {
    children: ["title", "base", "link", "style", "meta", "script", "noscript", "command"]
  },
  header: S,
  hgroup: S,
  hr: S,
  html: {
    attrs: { manifest: null }
  },
  i: S,
  iframe: {
    attrs: {
      src: null,
      srcdoc: null,
      name: null,
      width: null,
      height: null,
      sandbox: ["allow-top-navigation", "allow-same-origin", "allow-forms", "allow-scripts"],
      seamless: ["seamless"]
    }
  },
  img: {
    attrs: {
      alt: null,
      src: null,
      ismap: null,
      usemap: null,
      width: null,
      height: null,
      crossorigin: ["anonymous", "use-credentials"]
    }
  },
  input: {
    attrs: {
      alt: null,
      dirname: null,
      form: null,
      formaction: null,
      height: null,
      list: null,
      max: null,
      maxlength: null,
      min: null,
      name: null,
      pattern: null,
      placeholder: null,
      size: null,
      src: null,
      step: null,
      value: null,
      width: null,
      accept: ["audio/*", "video/*", "image/*"],
      autocomplete: ["on", "off"],
      autofocus: ["autofocus"],
      checked: ["checked"],
      disabled: ["disabled"],
      formenctype: Encs,
      formmethod: Methods,
      formnovalidate: ["novalidate"],
      formtarget: Targets,
      multiple: ["multiple"],
      readonly: ["readonly"],
      required: ["required"],
      type: [
        "hidden",
        "text",
        "search",
        "tel",
        "url",
        "email",
        "password",
        "datetime",
        "date",
        "month",
        "week",
        "time",
        "datetime-local",
        "number",
        "range",
        "color",
        "checkbox",
        "radio",
        "file",
        "submit",
        "image",
        "reset",
        "button"
      ]
    }
  },
  ins: { attrs: { cite: null, datetime: null } },
  kbd: S,
  keygen: {
    attrs: {
      challenge: null,
      form: null,
      name: null,
      autofocus: ["autofocus"],
      disabled: ["disabled"],
      keytype: ["RSA"]
    }
  },
  label: { attrs: { for: null, form: null } },
  legend: S,
  li: { attrs: { value: null } },
  link: {
    attrs: {
      href: null,
      type: null,
      hreflang: null,
      media: null,
      sizes: ["all", "16x16", "16x16 32x32", "16x16 32x32 64x64"]
    }
  },
  map: { attrs: { name: null } },
  mark: S,
  menu: { attrs: { label: null, type: ["list", "context", "toolbar"] } },
  meta: {
    attrs: {
      content: null,
      charset: Charsets,
      name: ["viewport", "application-name", "author", "description", "generator", "keywords"],
      "http-equiv": ["content-language", "content-type", "default-style", "refresh"]
    }
  },
  meter: { attrs: { value: null, min: null, low: null, high: null, max: null, optimum: null } },
  nav: S,
  noscript: S,
  object: {
    attrs: {
      data: null,
      type: null,
      name: null,
      usemap: null,
      form: null,
      width: null,
      height: null,
      typemustmatch: ["typemustmatch"]
    }
  },
  ol: {
    attrs: { reversed: ["reversed"], start: null, type: ["1", "a", "A", "i", "I"] },
    children: ["li", "script", "template", "ul", "ol"]
  },
  optgroup: { attrs: { disabled: ["disabled"], label: null } },
  option: { attrs: { disabled: ["disabled"], label: null, selected: ["selected"], value: null } },
  output: { attrs: { for: null, form: null, name: null } },
  p: S,
  param: { attrs: { name: null, value: null } },
  pre: S,
  progress: { attrs: { value: null, max: null } },
  q: { attrs: { cite: null } },
  rp: S,
  rt: S,
  ruby: S,
  samp: S,
  script: {
    attrs: {
      type: ["text/javascript"],
      src: null,
      async: ["async"],
      defer: ["defer"],
      charset: Charsets
    }
  },
  section: S,
  select: {
    attrs: {
      form: null,
      name: null,
      size: null,
      autofocus: ["autofocus"],
      disabled: ["disabled"],
      multiple: ["multiple"]
    }
  },
  slot: { attrs: { name: null } },
  small: S,
  source: { attrs: { src: null, type: null, media: null } },
  span: S,
  strong: S,
  style: {
    attrs: {
      type: ["text/css"],
      media: null,
      scoped: null
    }
  },
  sub: S,
  summary: S,
  sup: S,
  table: S,
  tbody: S,
  td: { attrs: { colspan: null, rowspan: null, headers: null } },
  template: S,
  textarea: {
    attrs: {
      dirname: null,
      form: null,
      maxlength: null,
      name: null,
      placeholder: null,
      rows: null,
      cols: null,
      autofocus: ["autofocus"],
      disabled: ["disabled"],
      readonly: ["readonly"],
      required: ["required"],
      wrap: ["soft", "hard"]
    }
  },
  tfoot: S,
  th: { attrs: { colspan: null, rowspan: null, headers: null, scope: ["row", "col", "rowgroup", "colgroup"] } },
  thead: S,
  time: { attrs: { datetime: null } },
  title: S,
  tr: S,
  track: {
    attrs: {
      src: null,
      label: null,
      default: null,
      kind: ["subtitles", "captions", "descriptions", "chapters", "metadata"],
      srclang: null
    }
  },
  ul: { children: ["li", "script", "template", "ul", "ol"] },
  var: S,
  video: {
    attrs: {
      src: null,
      poster: null,
      width: null,
      height: null,
      crossorigin: ["anonymous", "use-credentials"],
      preload: ["auto", "metadata", "none"],
      autoplay: ["autoplay"],
      mediagroup: ["movie"],
      muted: ["muted"],
      controls: ["controls"]
    }
  },
  wbr: S
};
const GlobalAttrs = {
  accesskey: null,
  class: null,
  contenteditable: Bool,
  contextmenu: null,
  dir: ["ltr", "rtl", "auto"],
  draggable: ["true", "false", "auto"],
  dropzone: ["copy", "move", "link", "string:", "file:"],
  hidden: ["hidden"],
  id: null,
  inert: ["inert"],
  itemid: null,
  itemprop: null,
  itemref: null,
  itemscope: ["itemscope"],
  itemtype: null,
  lang: ["ar", "bn", "de", "en-GB", "en-US", "es", "fr", "hi", "id", "ja", "pa", "pt", "ru", "tr", "zh"],
  spellcheck: Bool,
  autocorrect: Bool,
  autocapitalize: Bool,
  style: null,
  tabindex: null,
  title: null,
  translate: ["yes", "no"],
  rel: ["stylesheet", "alternate", "author", "bookmark", "help", "license", "next", "nofollow", "noreferrer", "prefetch", "prev", "search", "tag"],
  role: /* @__PURE__ */ "alert application article banner button cell checkbox complementary contentinfo dialog document feed figure form grid gridcell heading img list listbox listitem main navigation region row rowgroup search switch tab table tabpanel textbox timer".split(" "),
  "aria-activedescendant": null,
  "aria-atomic": Bool,
  "aria-autocomplete": ["inline", "list", "both", "none"],
  "aria-busy": Bool,
  "aria-checked": ["true", "false", "mixed", "undefined"],
  "aria-controls": null,
  "aria-describedby": null,
  "aria-disabled": Bool,
  "aria-dropeffect": null,
  "aria-expanded": ["true", "false", "undefined"],
  "aria-flowto": null,
  "aria-grabbed": ["true", "false", "undefined"],
  "aria-haspopup": Bool,
  "aria-hidden": Bool,
  "aria-invalid": ["true", "false", "grammar", "spelling"],
  "aria-label": null,
  "aria-labelledby": null,
  "aria-level": null,
  "aria-live": ["off", "polite", "assertive"],
  "aria-multiline": Bool,
  "aria-multiselectable": Bool,
  "aria-owns": null,
  "aria-posinset": null,
  "aria-pressed": ["true", "false", "mixed", "undefined"],
  "aria-readonly": Bool,
  "aria-relevant": null,
  "aria-required": Bool,
  "aria-selected": ["true", "false", "undefined"],
  "aria-setsize": null,
  "aria-sort": ["ascending", "descending", "none", "other"],
  "aria-valuemax": null,
  "aria-valuemin": null,
  "aria-valuenow": null,
  "aria-valuetext": null
};
const eventAttributes = /* @__PURE__ */ "beforeunload copy cut dragstart dragover dragleave dragenter dragend drag paste focus blur change click load mousedown mouseenter mouseleave mouseup keydown keyup resize scroll unload".split(" ").map((n) => "on" + n);
for (let a of eventAttributes)
  GlobalAttrs[a] = null;
class Schema {
  constructor(extraTags, extraAttrs) {
    this.tags = Object.assign(Object.assign({}, Tags), extraTags);
    this.globalAttrs = Object.assign(Object.assign({}, GlobalAttrs), extraAttrs);
    this.allTags = Object.keys(this.tags);
    this.globalAttrNames = Object.keys(this.globalAttrs);
  }
}
Schema.default = /* @__PURE__ */ new Schema();
function elementName(doc, tree, max = doc.length) {
  if (!tree)
    return "";
  let tag = tree.firstChild;
  let name = tag && tag.getChild("TagName");
  return name ? doc.sliceString(name.from, Math.min(name.to, max)) : "";
}
function findParentElement(tree, skip = false) {
  for (let cur = tree.parent; cur; cur = cur.parent)
    if (cur.name == "Element") {
      if (skip)
        skip = false;
      else
        return cur;
    }
  return null;
}
function allowedChildren(doc, tree, schema) {
  let parentInfo = schema.tags[elementName(doc, findParentElement(tree, true))];
  return (parentInfo === null || parentInfo === void 0 ? void 0 : parentInfo.children) || schema.allTags;
}
function openTags(doc, tree) {
  let open = [];
  for (let parent = tree; parent = findParentElement(parent); ) {
    let tagName = elementName(doc, parent);
    if (tagName && parent.lastChild.name == "CloseTag")
      break;
    if (tagName && open.indexOf(tagName) < 0 && (tree.name == "EndTag" || tree.from >= parent.firstChild.to))
      open.push(tagName);
  }
  return open;
}
const identifier = /^[:\-\.\w\u00b7-\uffff]*$/;
function completeTag(state, schema, tree, from, to) {
  let end = /\s*>/.test(state.sliceDoc(to, to + 5)) ? "" : ">";
  return {
    from,
    to,
    options: allowedChildren(state.doc, tree, schema).map((tagName) => ({ label: tagName, type: "type" })).concat(openTags(state.doc, tree).map((tag, i) => ({
      label: "/" + tag,
      apply: "/" + tag + end,
      type: "type",
      boost: 99 - i
    }))),
    validFor: /^\/?[:\-\.\w\u00b7-\uffff]*$/
  };
}
function completeCloseTag(state, tree, from, to) {
  let end = /\s*>/.test(state.sliceDoc(to, to + 5)) ? "" : ">";
  return {
    from,
    to,
    options: openTags(state.doc, tree).map((tag, i) => ({ label: tag, apply: tag + end, type: "type", boost: 99 - i })),
    validFor: identifier
  };
}
function completeStartTag(state, schema, tree, pos) {
  let options = [], level = 0;
  for (let tagName of allowedChildren(state.doc, tree, schema))
    options.push({ label: "<" + tagName, type: "type" });
  for (let open of openTags(state.doc, tree))
    options.push({ label: "</" + open + ">", type: "type", boost: 99 - level++ });
  return { from: pos, to: pos, options, validFor: /^<\/?[:\-\.\w\u00b7-\uffff]*$/ };
}
function completeAttrName(state, schema, tree, from, to) {
  let elt = findParentElement(tree), info = elt ? schema.tags[elementName(state.doc, elt)] : null;
  let localAttrs = info && info.attrs ? Object.keys(info.attrs) : [];
  let names = info && info.globalAttrs === false ? localAttrs : localAttrs.length ? localAttrs.concat(schema.globalAttrNames) : schema.globalAttrNames;
  return {
    from,
    to,
    options: names.map((attrName) => ({ label: attrName, type: "property" })),
    validFor: identifier
  };
}
function completeAttrValue(state, schema, tree, from, to) {
  var _a;
  let nameNode = (_a = tree.parent) === null || _a === void 0 ? void 0 : _a.getChild("AttributeName");
  let options = [], token = void 0;
  if (nameNode) {
    let attrName = state.sliceDoc(nameNode.from, nameNode.to);
    let attrs = schema.globalAttrs[attrName];
    if (!attrs) {
      let elt = findParentElement(tree), info = elt ? schema.tags[elementName(state.doc, elt)] : null;
      attrs = (info === null || info === void 0 ? void 0 : info.attrs) && info.attrs[attrName];
    }
    if (attrs) {
      let base = state.sliceDoc(from, to).toLowerCase(), quoteStart = '"', quoteEnd = '"';
      if (/^['"]/.test(base)) {
        token = base[0] == '"' ? /^[^"]*$/ : /^[^']*$/;
        quoteStart = "";
        quoteEnd = state.sliceDoc(to, to + 1) == base[0] ? "" : base[0];
        base = base.slice(1);
        from++;
      } else {
        token = /^[^\s<>='"]*$/;
      }
      for (let value of attrs)
        options.push({ label: value, apply: quoteStart + value + quoteEnd, type: "constant" });
    }
  }
  return { from, to, options, validFor: token };
}
function htmlCompletionFor(schema, context) {
  let { state, pos } = context, around = syntaxTree(state).resolveInner(pos), tree = around.resolve(pos, -1);
  for (let scan = pos, before; around == tree && (before = tree.childBefore(scan)); ) {
    let last = before.lastChild;
    if (!last || !last.type.isError || last.from < last.to)
      break;
    around = tree = before;
    scan = last.from;
  }
  if (tree.name == "TagName") {
    return tree.parent && /CloseTag$/.test(tree.parent.name) ? completeCloseTag(state, tree, tree.from, pos) : completeTag(state, schema, tree, tree.from, pos);
  } else if (tree.name == "StartTag") {
    return completeTag(state, schema, tree, pos, pos);
  } else if (tree.name == "StartCloseTag" || tree.name == "IncompleteCloseTag") {
    return completeCloseTag(state, tree, pos, pos);
  } else if (context.explicit && (tree.name == "OpenTag" || tree.name == "SelfClosingTag") || tree.name == "AttributeName") {
    return completeAttrName(state, schema, tree, tree.name == "AttributeName" ? tree.from : pos, pos);
  } else if (tree.name == "Is" || tree.name == "AttributeValue" || tree.name == "UnquotedAttributeValue") {
    return completeAttrValue(state, schema, tree, tree.name == "Is" ? pos : tree.from, pos);
  } else if (context.explicit && (around.name == "Element" || around.name == "Text" || around.name == "Document")) {
    return completeStartTag(state, schema, tree, pos);
  } else {
    return null;
  }
}
function htmlCompletionSource(context) {
  return htmlCompletionFor(Schema.default, context);
}
function htmlCompletionSourceWith(config) {
  let { extraTags, extraGlobalAttributes: extraAttrs } = config;
  let schema = extraAttrs || extraTags ? new Schema(extraTags, extraAttrs) : Schema.default;
  return (context) => htmlCompletionFor(schema, context);
}
const defaultNesting = [
  {
    tag: "script",
    attrs: (attrs) => attrs.type == "text/typescript" || attrs.lang == "ts",
    parser: typescriptLanguage.parser
  },
  {
    tag: "script",
    attrs: (attrs) => attrs.type == "text/babel" || attrs.type == "text/jsx",
    parser: jsxLanguage.parser
  },
  {
    tag: "script",
    attrs: (attrs) => attrs.type == "text/typescript-jsx",
    parser: tsxLanguage.parser
  },
  {
    tag: "script",
    attrs(attrs) {
      return !attrs.type || /^(?:text|application)\/(?:x-)?(?:java|ecma)script$|^module$|^$/i.test(attrs.type);
    },
    parser: javascriptLanguage.parser
  },
  {
    tag: "style",
    attrs(attrs) {
      return (!attrs.lang || attrs.lang == "css") && (!attrs.type || /^(text\/)?(x-)?(stylesheet|css)$/i.test(attrs.type));
    },
    parser: cssLanguage.parser
  }
];
const defaultAttrs = /* @__PURE__ */ [
  {
    name: "style",
    parser: /* @__PURE__ */ cssLanguage.parser.configure({ top: "Styles" })
  }
].concat(/* @__PURE__ */ eventAttributes.map((name) => ({ name, parser: javascriptLanguage.parser })));
const htmlLanguage = /* @__PURE__ */ LRLanguage.define({
  name: "html",
  parser: /* @__PURE__ */ parser.configure({
    props: [
      /* @__PURE__ */ indentNodeProp.add({
        Element(context) {
          let after = /^(\s*)(<\/)?/.exec(context.textAfter);
          if (context.node.to <= context.pos + after[0].length)
            return context.continue();
          return context.lineIndent(context.node.from) + (after[2] ? 0 : context.unit);
        },
        "OpenTag CloseTag SelfClosingTag"(context) {
          return context.column(context.node.from) + context.unit;
        },
        Document(context) {
          if (context.pos + /\s*/.exec(context.textAfter)[0].length < context.node.to)
            return context.continue();
          let endElt = null, close;
          for (let cur = context.node; ; ) {
            let last = cur.lastChild;
            if (!last || last.name != "Element" || last.to != cur.to)
              break;
            endElt = cur = last;
          }
          if (endElt && !((close = endElt.lastChild) && (close.name == "CloseTag" || close.name == "SelfClosingTag")))
            return context.lineIndent(endElt.from) + context.unit;
          return null;
        }
      }),
      /* @__PURE__ */ foldNodeProp.add({
        Element(node) {
          let first = node.firstChild, last = node.lastChild;
          if (!first || first.name != "OpenTag")
            return null;
          return { from: first.to, to: last.name == "CloseTag" ? last.from : node.to };
        }
      }),
      /* @__PURE__ */ bracketMatchingHandle.add({
        "OpenTag CloseTag": (node) => node.getChild("TagName")
      })
    ],
    wrap: /* @__PURE__ */ configureNesting(defaultNesting, defaultAttrs)
  }),
  languageData: {
    commentTokens: { block: { open: "<!--", close: "-->" } },
    indentOnInput: /^\s*<\/\w+\W$/,
    wordChars: "-._"
  }
});
function html(config = {}) {
  let dialect = "", wrap;
  if (config.matchClosingTags === false)
    dialect = "noMatch";
  if (config.selfClosingTags === true)
    dialect = (dialect ? dialect + " " : "") + "selfClosing";
  if (config.nestedLanguages && config.nestedLanguages.length || config.nestedAttributes && config.nestedAttributes.length)
    wrap = configureNesting((config.nestedLanguages || []).concat(defaultNesting), (config.nestedAttributes || []).concat(defaultAttrs));
  let lang = wrap || dialect ? htmlLanguage.configure({ dialect, wrap }) : htmlLanguage;
  return new LanguageSupport(lang, [
    htmlLanguage.data.of({ autocomplete: htmlCompletionSourceWith(config) }),
    config.autoCloseTags !== false ? autoCloseTags : [],
    javascript().support,
    css().support
  ]);
}
const selfClosers = /* @__PURE__ */ new Set(/* @__PURE__ */ "area base br col command embed frame hr img input keygen link meta param source track wbr menuitem".split(" "));
const autoCloseTags = /* @__PURE__ */ EditorView.inputHandler.of((view, from, to, text) => {
  if (view.composing || view.state.readOnly || from != to || text != ">" && text != "/" || !htmlLanguage.isActiveAt(view.state, from, -1))
    return false;
  let { state } = view;
  let changes = state.changeByRange((range) => {
    var _a, _b, _c;
    let { head } = range, around = syntaxTree(state).resolveInner(head, -1), name;
    if (around.name == "TagName" || around.name == "StartTag")
      around = around.parent;
    if (text == ">" && around.name == "OpenTag") {
      if (((_b = (_a = around.parent) === null || _a === void 0 ? void 0 : _a.lastChild) === null || _b === void 0 ? void 0 : _b.name) != "CloseTag" && (name = elementName(state.doc, around.parent, head)) && !selfClosers.has(name)) {
        let hasRightBracket = view.state.doc.sliceString(head, head + 1) === ">";
        let insert = `${hasRightBracket ? "" : ">"}</${name}>`;
        return { range: EditorSelection.cursor(head + 1), changes: { from: head + (hasRightBracket ? 1 : 0), insert } };
      }
    } else if (text == "/" && around.name == "OpenTag") {
      let empty = around.parent, base = empty === null || empty === void 0 ? void 0 : empty.parent;
      if (empty.from == head - 1 && ((_c = base.lastChild) === null || _c === void 0 ? void 0 : _c.name) != "CloseTag" && (name = elementName(state.doc, base, head)) && !selfClosers.has(name)) {
        let hasRightBracket = view.state.doc.sliceString(head, head + 1) === ">";
        let insert = `/${name}${hasRightBracket ? "" : ">"}`;
        let pos = head + insert.length + (hasRightBracket ? 1 : 0);
        return { range: EditorSelection.cursor(pos), changes: { from: head, insert } };
      }
    }
    return { range };
  });
  if (changes.changes.empty)
    return false;
  view.dispatch(changes, { userEvent: "input.type", scrollIntoView: true });
  return true;
});

export { autoCloseTags, html, htmlCompletionSource, htmlCompletionSourceWith, htmlLanguage };
//# sourceMappingURL=index33-Dw5RSZZD.js.map
