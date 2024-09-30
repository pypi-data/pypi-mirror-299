import { E as ExternalTokenizer, L as LRParser, a as LocalTokenGroup } from './index18-Bk6aUetb.js';
import { s as styleTags, t as tags$1, h as syntaxTree, L as LRLanguage, i as indentNodeProp, w as continuedIndent, f as foldNodeProp, c as foldInside, e as LanguageSupport, I as IterMode, x as NodeWeakMap } from './Index19-Ct8qgVF0.js';
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

const descendantOp = 96, Unit = 1, callee = 97, identifier$1 = 98, VariableName = 2;
const space = [
  9,
  10,
  11,
  12,
  13,
  32,
  133,
  160,
  5760,
  8192,
  8193,
  8194,
  8195,
  8196,
  8197,
  8198,
  8199,
  8200,
  8201,
  8202,
  8232,
  8233,
  8239,
  8287,
  12288
];
const colon = 58, parenL = 40, underscore = 95, bracketL = 91, dash = 45, period = 46, hash = 35, percent = 37, ampersand = 38, backslash = 92, newline = 10;
function isAlpha(ch) {
  return ch >= 65 && ch <= 90 || ch >= 97 && ch <= 122 || ch >= 161;
}
function isDigit(ch) {
  return ch >= 48 && ch <= 57;
}
const identifiers = new ExternalTokenizer((input, stack) => {
  for (let inside = false, dashes = 0, i = 0; ; i++) {
    let { next } = input;
    if (isAlpha(next) || next == dash || next == underscore || inside && isDigit(next)) {
      if (!inside && (next != dash || i > 0))
        inside = true;
      if (dashes === i && next == dash)
        dashes++;
      input.advance();
    } else if (next == backslash && input.peek(1) != newline) {
      input.advance();
      if (input.next > -1)
        input.advance();
      inside = true;
    } else {
      if (inside)
        input.acceptToken(next == parenL ? callee : dashes == 2 && stack.canShift(VariableName) ? VariableName : identifier$1);
      break;
    }
  }
});
const descendant = new ExternalTokenizer((input) => {
  if (space.includes(input.peek(-1))) {
    let { next } = input;
    if (isAlpha(next) || next == underscore || next == hash || next == period || next == bracketL || next == colon || next == dash || next == ampersand)
      input.acceptToken(descendantOp);
  }
});
const unitToken = new ExternalTokenizer((input) => {
  if (!space.includes(input.peek(-1))) {
    let { next } = input;
    if (next == percent) {
      input.advance();
      input.acceptToken(Unit);
    }
    if (isAlpha(next)) {
      do {
        input.advance();
      } while (isAlpha(input.next));
      input.acceptToken(Unit);
    }
  }
});
const cssHighlighting = styleTags({
  "AtKeyword import charset namespace keyframes media supports": tags$1.definitionKeyword,
  "from to selector": tags$1.keyword,
  NamespaceName: tags$1.namespace,
  KeyframeName: tags$1.labelName,
  KeyframeRangeName: tags$1.operatorKeyword,
  TagName: tags$1.tagName,
  ClassName: tags$1.className,
  PseudoClassName: tags$1.constant(tags$1.className),
  IdName: tags$1.labelName,
  "FeatureName PropertyName": tags$1.propertyName,
  AttributeName: tags$1.attributeName,
  NumberLiteral: tags$1.number,
  KeywordQuery: tags$1.keyword,
  UnaryQueryOp: tags$1.operatorKeyword,
  "CallTag ValueName": tags$1.atom,
  VariableName: tags$1.variableName,
  Callee: tags$1.operatorKeyword,
  Unit: tags$1.unit,
  "UniversalSelector NestingSelector": tags$1.definitionOperator,
  MatchOp: tags$1.compareOperator,
  "ChildOp SiblingOp, LogicOp": tags$1.logicOperator,
  BinOp: tags$1.arithmeticOperator,
  Important: tags$1.modifier,
  Comment: tags$1.blockComment,
  ColorLiteral: tags$1.color,
  "ParenthesizedContent StringLiteral": tags$1.string,
  ":": tags$1.punctuation,
  "PseudoOp #": tags$1.derefOperator,
  "; ,": tags$1.separator,
  "( )": tags$1.paren,
  "[ ]": tags$1.squareBracket,
  "{ }": tags$1.brace
});
const spec_callee = { __proto__: null, lang: 32, "nth-child": 32, "nth-last-child": 32, "nth-of-type": 32, "nth-last-of-type": 32, dir: 32, "host-context": 32, url: 60, "url-prefix": 60, domain: 60, regexp: 60, selector: 134 };
const spec_AtKeyword = { __proto__: null, "@import": 114, "@media": 138, "@charset": 142, "@namespace": 146, "@keyframes": 152, "@supports": 164 };
const spec_identifier = { __proto__: null, not: 128, only: 128 };
const parser = LRParser.deserialize({
  version: 14,
  states: "9bQYQ[OOO#_Q[OOP#fOWOOOOQP'#Cd'#CdOOQP'#Cc'#CcO#kQ[O'#CfO$_QXO'#CaO$fQ[O'#ChO$qQ[O'#DPO$vQ[O'#DTOOQP'#Ej'#EjO${QdO'#DeO%gQ[O'#DrO${QdO'#DtO%xQ[O'#DvO&TQ[O'#DyO&]Q[O'#EPO&kQ[O'#EROOQS'#Ei'#EiOOQS'#EU'#EUQYQ[OOO&rQXO'#CdO'gQWO'#DaO'lQWO'#EpO'wQ[O'#EpQOQWOOP(RO#tO'#C_POOO)C@X)C@XOOQP'#Cg'#CgOOQP,59Q,59QO#kQ[O,59QO(^Q[O'#EXO(xQWO,58{O)QQ[O,59SO$qQ[O,59kO$vQ[O,59oO(^Q[O,59sO(^Q[O,59uO(^Q[O,59vO)]Q[O'#D`OOQS,58{,58{OOQP'#Ck'#CkOOQO'#C}'#C}OOQP,59S,59SO)dQWO,59SO)iQWO,59SOOQP'#DR'#DROOQP,59k,59kOOQO'#DV'#DVO)nQ`O,59oOOQS'#Cp'#CpO${QdO'#CqO)vQvO'#CsO+TQtO,5:POOQO'#Cx'#CxO)iQWO'#CwO+iQWO'#CyOOQS'#Em'#EmOOQO'#Dh'#DhO+nQ[O'#DoO+|QWO'#EqO&]Q[O'#DmO,[QWO'#DpOOQO'#Er'#ErO({QWO,5:^O,aQpO,5:`OOQS'#Dx'#DxO,iQWO,5:bO,nQ[O,5:bOOQO'#D{'#D{O,vQWO,5:eO,{QWO,5:kO-TQWO,5:mOOQS-E8S-E8SO${QdO,59{O-]Q[O'#EZO-jQWO,5;[O-jQWO,5;[POOO'#ET'#ETP-uO#tO,58yPOOO,58y,58yOOQP1G.l1G.lO.lQXO,5:sOOQO-E8V-E8VOOQS1G.g1G.gOOQP1G.n1G.nO)dQWO1G.nO)iQWO1G.nOOQP1G/V1G/VO.yQ`O1G/ZO/dQXO1G/_O/zQXO1G/aO0bQXO1G/bO0xQWO,59zO0}Q[O'#DOO1UQdO'#CoOOQP1G/Z1G/ZO${QdO1G/ZO1]QpO,59]OOQS,59_,59_O${QdO,59aO1eQWO1G/kOOQS,59c,59cO1jQ!bO,59eO1rQWO'#DhO1}QWO,5:TO2SQWO,5:ZO&]Q[O,5:VO&]Q[O'#E[O2[QWO,5;]O2gQWO,5:XO(^Q[O,5:[OOQS1G/x1G/xOOQS1G/z1G/zOOQS1G/|1G/|O2xQWO1G/|O2}QdO'#D|OOQS1G0P1G0POOQS1G0V1G0VOOQS1G0X1G0XO3YQtO1G/gOOQO,5:u,5:uO3pQ[O,5:uOOQO-E8X-E8XO3}QWO1G0vPOOO-E8R-E8RPOOO1G.e1G.eOOQP7+$Y7+$YOOQP7+$u7+$uO${QdO7+$uOOQS1G/f1G/fO4YQXO'#EoO4aQWO,59jO4fQtO'#EVO5ZQdO'#ElO5eQWO,59ZO5jQpO7+$uOOQS1G.w1G.wOOQS1G.{1G.{OOQS7+%V7+%VO5rQWO1G/PO${QdO1G/oOOQO1G/u1G/uOOQO1G/q1G/qO5wQWO,5:vOOQO-E8Y-E8YO6VQXO1G/vOOQS7+%h7+%hO6^QYO'#CsOOQO'#EO'#EOO6iQ`O'#D}OOQO'#D}'#D}O6tQWO'#E]O6|QdO,5:hOOQS,5:h,5:hO7XQtO'#EYO${QdO'#EYO8VQdO7+%ROOQO7+%R7+%ROOQO1G0a1G0aO8jQpO<<HaO8rQWO,5;ZOOQP1G/U1G/UOOQS-E8T-E8TO${QdO'#EWO8zQWO,5;WOOQT1G.u1G.uOOQP<<Ha<<HaOOQS7+$k7+$kO9SQdO7+%ZOOQO7+%b7+%bOOQO,5:i,5:iO3QQdO'#E^O6tQWO,5:wOOQS,5:w,5:wOOQS-E8Z-E8ZOOQS1G0S1G0SO9ZQtO,5:tOOQS-E8W-E8WOOQO<<Hm<<HmOOQPAN={AN={O:XQdO,5:rOOQO-E8U-E8UOOQO<<Hu<<HuOOQO,5:x,5:xOOQO-E8[-E8[OOQS1G0c1G0c",
  stateData: ":k~O#WOS#XQQ~OUYOXYO]VO^VOtWOxXO!YaO!ZZO!g[O!i]O!k^O!n_O!t`O#URO#_TO~OQfOUYOXYO]VO^VOtWOxXO!YaO!ZZO!g[O!i]O!k^O!n_O!t`O#UeO#_TO~O#R#dP~P!ZO#XjO~O#UlO~O]qO^qOpoOtrOxsO|tO!PvO#SuO#_nO~O!RwO~P#pO`}O#TzO#UyO~O#U!OO~O#U!QO~OQ!ZOb!TOf!ZOh!ZOn!YO#T!WO#U!SO#b!UO~Ob!]O!b!_O!e!`O#U![O!R#eP~Oh!eOn!YO#U!dO~Oh!gO#U!gO~Ob!]O!b!_O!e!`O#U![O~O!W#eP~P%gO]WX]!UX^WXpWXtWXxWX|WX!PWX!RWX#SWX#_WX~O]!lO~O!W!mO#R#dX!Q#dX~O#R#dX!Q#dX~P!ZO#Y!pO#Z!pO#[!rO~OUYOXYO]VO^VOtWOxXO#URO#_TO~OpoO!RwO~O`!yO#TzO#UyO~O!Q#dP~P!ZOb#QO~Ob#RO~Ov#SOz#TO~OP#VObgXjgX!WgX!bgX!egX#UgXagXQgXfgXhgXngXpgX!VgX#RgX#TgX#bgXvgX!QgX~Ob!]Oj#WO!b!_O!e!`O#U![O!W#eP~Ob#ZO~Ob!]O!b!_O!e!`O#U#[O~Op#`O!`#_O!R#eX!W#eX~Ob#cO~Oj#WO!W#eO~O!W#fO~Oh#gOn!YO~O!R#hO~O!RwO!`#_O~O!RwO!W#kO~O!W!}X#R!}X!Q!}X~P!ZO!W!mO#R#da!Q#da~O#Y!pO#Z!pO#[#rO~O]qO^qOtrOxsO|tO!PvO#SuO#_nO~Op!{a!R!{aa!{a~P.QOv#tOz#uO~O]qO^qOtrOxsO#_nO~Op{i|{i!P{i!R{i#S{ia{i~P/ROp}i|}i!P}i!R}i#S}ia}i~P/ROp!Oi|!Oi!P!Oi!R!Oi#S!Oia!Oi~P/RO!Q#vO~Oa#cP~P(^Oa#`P~P${Oa#}Oj#WO~O!W$PO~Oh$QOo$QO~O]!^Xa![X!`![X~O]$RO~Oa$SO!`#_O~Op#`O!R#ea!W#ea~O!`#_Op!aa!R!aa!W!aaa!aa~O!W$XO~O!Q$`O#U$ZO#b$YO~Oj#WOp$bO!V$dO!W!Ti#R!Ti!Q!Ti~P${O!W!}a#R!}a!Q!}a~P!ZO!W!mO#R#di!Q#di~Oa#cX~P#pOa$hO~Oj#WOQ!yXa!yXb!yXf!yXh!yXn!yXp!yX#T!yX#U!yX#b!yX~Op$jOa#`X~P${Oa$lO~Oj#WOv$mO~Oa$nO~O!`#_Op#Oa!R#Oa!W#Oa~Oa$pO~P.QOP#VOpgX!RgX~O#b$YOp!qX!R!qX~Op$rO!RwO~O!Q$vO#U$ZO#b$YO~Oj#WOQ!|Xb!|Xf!|Xh!|Xn!|Xp!|X!V!|X!W!|X#R!|X#T!|X#U!|X#b!|X!Q!|X~Op$bO!V$yO!W!Tq#R!Tq!Q!Tq~P${Oj#WOv$zO~OpoOa#ca~Op$jOa#`a~Oa$}O~P${Oj#WOQ!|ab!|af!|ah!|an!|ap!|a!V!|a!W!|a#R!|a#T!|a#U!|a#b!|a!Q!|a~Oa!zap!za~P${O#Wo#X#bj!P#b~",
  goto: "-Y#gPPP#hP#kP#t$TP#t$d#tPP$jPPP$p$y$yP%]P$yP$y%w&ZPPP&s&y#tP'PP#tP'VP#tP#t#tPPP']'r(PPP#kPP(W(W(b(WP(WP(W(WP#kP#kP#kP(e#kP(h(k(n(u#kP#kP(z)Q)a)o)u*P*V*a*g*mPPPPPPPPPP*s*|P+i+lP,b,e,k,tRkQ_bOPdhw!m#nkYOPdhotuvw!m#Q#c#nkSOPdhotuvw!m#Q#c#nQmTR!snQ{VR!wqQ!w}Q#Y!XR#s!yq!ZZ]!T!l#R#T#W#l#u#z$R$b$c$j$o${p!ZZ]!T!l#R#T#W#l#u#z$R$b$c$j$o${U$]#h$_$rR$q$[q!XZ]!T!l#R#T#W#l#u#z$R$b$c$j$o${p!ZZ]!T!l#R#T#W#l#u#z$R$b$c$j$o${Q!e^R#g!fQ|VR!xqQ!w|R#s!xQ!PWR!zrQ!RXR!{sQxUQ!vpQ#d!bQ#j!iQ#k!jQ$t$^R%Q$sSgPwQ!ohQ#m!mR$e#nZfPhw!m#na!a[`a!V!]!_#_#`R#]!]R!f^R!h_R#i!hS$^#h$_R%O$rV$[#h$_$rQ!qjR#q!qQdOShPwU!kdh#nR#n!mQ#z#RU$i#z$o${Q$o$RR${$jQ$k#zR$|$kQpUS!up$gR$g#wQ$c#lR$x$cQ!ngS#o!n#pR#p!oQ#a!^R$V#aQ$_#hR$u$_Q$s$^R%P$s_cOPdhw!m#n^UOPdhw!m#nQ!toQ!|tQ!}uQ#OvQ#w#QR$W#cR#{#RQ!VZQ!c]Q#U!TQ#l!l[#y#R#z$R$j$o${Q#|#TQ$O#WS$a#l$cQ$f#uR$w$bR#x#QQiPR#PwQ!b[Q!jaR#X!VU!^[a!VQ!i`Q#^!]Q#b!_Q$T#_R$U#`",
  nodeNames: "⚠ Unit VariableName Comment StyleSheet RuleSet UniversalSelector TagSelector TagName NestingSelector ClassSelector ClassName PseudoClassSelector : :: PseudoClassName PseudoClassName ) ( ArgList ValueName ParenthesizedValue ColorLiteral NumberLiteral StringLiteral BinaryExpression BinOp CallExpression Callee CallLiteral CallTag ParenthesizedContent , PseudoClassName ArgList IdSelector # IdName ] AttributeSelector [ AttributeName MatchOp ChildSelector ChildOp DescendantSelector SiblingSelector SiblingOp } { Block Declaration PropertyName Important ; ImportStatement AtKeyword import KeywordQuery FeatureQuery FeatureName BinaryQuery LogicOp UnaryQuery UnaryQueryOp ParenthesizedQuery SelectorQuery selector MediaStatement media CharsetStatement charset NamespaceStatement namespace NamespaceName KeyframesStatement keyframes KeyframeName KeyframeList KeyframeSelector KeyframeRangeName SupportsStatement supports AtRule Styles",
  maxTerm: 114,
  nodeProps: [
    ["openedBy", 17, "(", 48, "{"],
    ["closedBy", 18, ")", 49, "}"]
  ],
  propSources: [cssHighlighting],
  skippedNodes: [0, 3, 85],
  repeatNodeCount: 10,
  tokenData: "J^~R!^OX$}X^%u^p$}pq%uqr)Xrs.Rst/utu6duv$}vw7^wx7oxy9^yz9oz{9t{|:_|}?Q}!O?c!O!P@Q!P!Q@i!Q![Ab![!]B]!]!^CX!^!_$}!_!`Cj!`!aC{!a!b$}!b!cDw!c!}$}!}#OFa#O#P$}#P#QFr#Q#R6d#R#T$}#T#UGT#U#c$}#c#dHf#d#o$}#o#pH{#p#q6d#q#rI^#r#sIo#s#y$}#y#z%u#z$f$}$f$g%u$g#BY$}#BY#BZ%u#BZ$IS$}$IS$I_%u$I_$I|$}$I|$JO%u$JO$JT$}$JT$JU%u$JU$KV$}$KV$KW%u$KW&FU$}&FU&FV%u&FV;'S$};'S;=`JW<%lO$}`%QSOy%^z;'S%^;'S;=`%o<%lO%^`%cSo`Oy%^z;'S%^;'S;=`%o<%lO%^`%rP;=`<%l%^~%zh#W~OX%^X^'f^p%^pq'fqy%^z#y%^#y#z'f#z$f%^$f$g'f$g#BY%^#BY#BZ'f#BZ$IS%^$IS$I_'f$I_$I|%^$I|$JO'f$JO$JT%^$JT$JU'f$JU$KV%^$KV$KW'f$KW&FU%^&FU&FV'f&FV;'S%^;'S;=`%o<%lO%^~'mh#W~o`OX%^X^'f^p%^pq'fqy%^z#y%^#y#z'f#z$f%^$f$g'f$g#BY%^#BY#BZ'f#BZ$IS%^$IS$I_'f$I_$I|%^$I|$JO'f$JO$JT%^$JT$JU'f$JU$KV%^$KV$KW'f$KW&FU%^&FU&FV'f&FV;'S%^;'S;=`%o<%lO%^l)[UOy%^z#]%^#]#^)n#^;'S%^;'S;=`%o<%lO%^l)sUo`Oy%^z#a%^#a#b*V#b;'S%^;'S;=`%o<%lO%^l*[Uo`Oy%^z#d%^#d#e*n#e;'S%^;'S;=`%o<%lO%^l*sUo`Oy%^z#c%^#c#d+V#d;'S%^;'S;=`%o<%lO%^l+[Uo`Oy%^z#f%^#f#g+n#g;'S%^;'S;=`%o<%lO%^l+sUo`Oy%^z#h%^#h#i,V#i;'S%^;'S;=`%o<%lO%^l,[Uo`Oy%^z#T%^#T#U,n#U;'S%^;'S;=`%o<%lO%^l,sUo`Oy%^z#b%^#b#c-V#c;'S%^;'S;=`%o<%lO%^l-[Uo`Oy%^z#h%^#h#i-n#i;'S%^;'S;=`%o<%lO%^l-uS!V[o`Oy%^z;'S%^;'S;=`%o<%lO%^~.UWOY.RZr.Rrs.ns#O.R#O#P.s#P;'S.R;'S;=`/o<%lO.R~.sOh~~.vRO;'S.R;'S;=`/P;=`O.R~/SXOY.RZr.Rrs.ns#O.R#O#P.s#P;'S.R;'S;=`/o;=`<%l.R<%lO.R~/rP;=`<%l.Rn/zYtQOy%^z!Q%^!Q![0j![!c%^!c!i0j!i#T%^#T#Z0j#Z;'S%^;'S;=`%o<%lO%^l0oYo`Oy%^z!Q%^!Q![1_![!c%^!c!i1_!i#T%^#T#Z1_#Z;'S%^;'S;=`%o<%lO%^l1dYo`Oy%^z!Q%^!Q![2S![!c%^!c!i2S!i#T%^#T#Z2S#Z;'S%^;'S;=`%o<%lO%^l2ZYf[o`Oy%^z!Q%^!Q![2y![!c%^!c!i2y!i#T%^#T#Z2y#Z;'S%^;'S;=`%o<%lO%^l3QYf[o`Oy%^z!Q%^!Q![3p![!c%^!c!i3p!i#T%^#T#Z3p#Z;'S%^;'S;=`%o<%lO%^l3uYo`Oy%^z!Q%^!Q![4e![!c%^!c!i4e!i#T%^#T#Z4e#Z;'S%^;'S;=`%o<%lO%^l4lYf[o`Oy%^z!Q%^!Q![5[![!c%^!c!i5[!i#T%^#T#Z5[#Z;'S%^;'S;=`%o<%lO%^l5aYo`Oy%^z!Q%^!Q![6P![!c%^!c!i6P!i#T%^#T#Z6P#Z;'S%^;'S;=`%o<%lO%^l6WSf[o`Oy%^z;'S%^;'S;=`%o<%lO%^d6gUOy%^z!_%^!_!`6y!`;'S%^;'S;=`%o<%lO%^d7QSzSo`Oy%^z;'S%^;'S;=`%o<%lO%^b7cSXQOy%^z;'S%^;'S;=`%o<%lO%^~7rWOY7oZw7owx.nx#O7o#O#P8[#P;'S7o;'S;=`9W<%lO7o~8_RO;'S7o;'S;=`8h;=`O7o~8kXOY7oZw7owx.nx#O7o#O#P8[#P;'S7o;'S;=`9W;=`<%l7o<%lO7o~9ZP;=`<%l7on9cSb^Oy%^z;'S%^;'S;=`%o<%lO%^~9tOa~n9{UUQjWOy%^z!_%^!_!`6y!`;'S%^;'S;=`%o<%lO%^n:fWjW!PQOy%^z!O%^!O!P;O!P!Q%^!Q![>T![;'S%^;'S;=`%o<%lO%^l;TUo`Oy%^z!Q%^!Q![;g![;'S%^;'S;=`%o<%lO%^l;nYo`#b[Oy%^z!Q%^!Q![;g![!g%^!g!h<^!h#X%^#X#Y<^#Y;'S%^;'S;=`%o<%lO%^l<cYo`Oy%^z{%^{|=R|}%^}!O=R!O!Q%^!Q![=j![;'S%^;'S;=`%o<%lO%^l=WUo`Oy%^z!Q%^!Q![=j![;'S%^;'S;=`%o<%lO%^l=qUo`#b[Oy%^z!Q%^!Q![=j![;'S%^;'S;=`%o<%lO%^l>[[o`#b[Oy%^z!O%^!O!P;g!P!Q%^!Q![>T![!g%^!g!h<^!h#X%^#X#Y<^#Y;'S%^;'S;=`%o<%lO%^n?VSp^Oy%^z;'S%^;'S;=`%o<%lO%^l?hWjWOy%^z!O%^!O!P;O!P!Q%^!Q![>T![;'S%^;'S;=`%o<%lO%^n@VU#_QOy%^z!Q%^!Q![;g![;'S%^;'S;=`%o<%lO%^~@nTjWOy%^z{@}{;'S%^;'S;=`%o<%lO%^~AUSo`#X~Oy%^z;'S%^;'S;=`%o<%lO%^lAg[#b[Oy%^z!O%^!O!P;g!P!Q%^!Q![>T![!g%^!g!h<^!h#X%^#X#Y<^#Y;'S%^;'S;=`%o<%lO%^bBbU]QOy%^z![%^![!]Bt!];'S%^;'S;=`%o<%lO%^bB{S^Qo`Oy%^z;'S%^;'S;=`%o<%lO%^nC^S!W^Oy%^z;'S%^;'S;=`%o<%lO%^dCoSzSOy%^z;'S%^;'S;=`%o<%lO%^bDQU|QOy%^z!`%^!`!aDd!a;'S%^;'S;=`%o<%lO%^bDkS|Qo`Oy%^z;'S%^;'S;=`%o<%lO%^bDzWOy%^z!c%^!c!}Ed!}#T%^#T#oEd#o;'S%^;'S;=`%o<%lO%^bEk[!YQo`Oy%^z}%^}!OEd!O!Q%^!Q![Ed![!c%^!c!}Ed!}#T%^#T#oEd#o;'S%^;'S;=`%o<%lO%^bFfSxQOy%^z;'S%^;'S;=`%o<%lO%^lFwSv[Oy%^z;'S%^;'S;=`%o<%lO%^bGWUOy%^z#b%^#b#cGj#c;'S%^;'S;=`%o<%lO%^bGoUo`Oy%^z#W%^#W#XHR#X;'S%^;'S;=`%o<%lO%^bHYS!`Qo`Oy%^z;'S%^;'S;=`%o<%lO%^bHiUOy%^z#f%^#f#gHR#g;'S%^;'S;=`%o<%lO%^fIQS!RUOy%^z;'S%^;'S;=`%o<%lO%^nIcS!Q^Oy%^z;'S%^;'S;=`%o<%lO%^fItU!PQOy%^z!_%^!_!`6y!`;'S%^;'S;=`%o<%lO%^`JZP;=`<%l$}",
  tokenizers: [descendant, unitToken, identifiers, 1, 2, 3, 4, new LocalTokenGroup("m~RRYZ[z{a~~g~aO#Z~~dP!P!Qg~lO#[~~", 28, 102)],
  topRules: { "StyleSheet": [0, 4], "Styles": [1, 84] },
  specialized: [{ term: 97, get: (value) => spec_callee[value] || -1 }, { term: 56, get: (value) => spec_AtKeyword[value] || -1 }, { term: 98, get: (value) => spec_identifier[value] || -1 }],
  tokenPrec: 1169
});
let _properties = null;
function properties() {
  if (!_properties && typeof document == "object" && document.body) {
    let { style } = document.body, names = [], seen = /* @__PURE__ */ new Set();
    for (let prop in style)
      if (prop != "cssText" && prop != "cssFloat") {
        if (typeof style[prop] == "string") {
          if (/[A-Z]/.test(prop))
            prop = prop.replace(/[A-Z]/g, (ch) => "-" + ch.toLowerCase());
          if (!seen.has(prop)) {
            names.push(prop);
            seen.add(prop);
          }
        }
      }
    _properties = names.sort().map((name) => ({ type: "property", label: name }));
  }
  return _properties || [];
}
const pseudoClasses = /* @__PURE__ */ [
  "active",
  "after",
  "any-link",
  "autofill",
  "backdrop",
  "before",
  "checked",
  "cue",
  "default",
  "defined",
  "disabled",
  "empty",
  "enabled",
  "file-selector-button",
  "first",
  "first-child",
  "first-letter",
  "first-line",
  "first-of-type",
  "focus",
  "focus-visible",
  "focus-within",
  "fullscreen",
  "has",
  "host",
  "host-context",
  "hover",
  "in-range",
  "indeterminate",
  "invalid",
  "is",
  "lang",
  "last-child",
  "last-of-type",
  "left",
  "link",
  "marker",
  "modal",
  "not",
  "nth-child",
  "nth-last-child",
  "nth-last-of-type",
  "nth-of-type",
  "only-child",
  "only-of-type",
  "optional",
  "out-of-range",
  "part",
  "placeholder",
  "placeholder-shown",
  "read-only",
  "read-write",
  "required",
  "right",
  "root",
  "scope",
  "selection",
  "slotted",
  "target",
  "target-text",
  "valid",
  "visited",
  "where"
].map((name) => ({ type: "class", label: name }));
const values = /* @__PURE__ */ [
  "above",
  "absolute",
  "activeborder",
  "additive",
  "activecaption",
  "after-white-space",
  "ahead",
  "alias",
  "all",
  "all-scroll",
  "alphabetic",
  "alternate",
  "always",
  "antialiased",
  "appworkspace",
  "asterisks",
  "attr",
  "auto",
  "auto-flow",
  "avoid",
  "avoid-column",
  "avoid-page",
  "avoid-region",
  "axis-pan",
  "background",
  "backwards",
  "baseline",
  "below",
  "bidi-override",
  "blink",
  "block",
  "block-axis",
  "bold",
  "bolder",
  "border",
  "border-box",
  "both",
  "bottom",
  "break",
  "break-all",
  "break-word",
  "bullets",
  "button",
  "button-bevel",
  "buttonface",
  "buttonhighlight",
  "buttonshadow",
  "buttontext",
  "calc",
  "capitalize",
  "caps-lock-indicator",
  "caption",
  "captiontext",
  "caret",
  "cell",
  "center",
  "checkbox",
  "circle",
  "cjk-decimal",
  "clear",
  "clip",
  "close-quote",
  "col-resize",
  "collapse",
  "color",
  "color-burn",
  "color-dodge",
  "column",
  "column-reverse",
  "compact",
  "condensed",
  "contain",
  "content",
  "contents",
  "content-box",
  "context-menu",
  "continuous",
  "copy",
  "counter",
  "counters",
  "cover",
  "crop",
  "cross",
  "crosshair",
  "currentcolor",
  "cursive",
  "cyclic",
  "darken",
  "dashed",
  "decimal",
  "decimal-leading-zero",
  "default",
  "default-button",
  "dense",
  "destination-atop",
  "destination-in",
  "destination-out",
  "destination-over",
  "difference",
  "disc",
  "discard",
  "disclosure-closed",
  "disclosure-open",
  "document",
  "dot-dash",
  "dot-dot-dash",
  "dotted",
  "double",
  "down",
  "e-resize",
  "ease",
  "ease-in",
  "ease-in-out",
  "ease-out",
  "element",
  "ellipse",
  "ellipsis",
  "embed",
  "end",
  "ethiopic-abegede-gez",
  "ethiopic-halehame-aa-er",
  "ethiopic-halehame-gez",
  "ew-resize",
  "exclusion",
  "expanded",
  "extends",
  "extra-condensed",
  "extra-expanded",
  "fantasy",
  "fast",
  "fill",
  "fill-box",
  "fixed",
  "flat",
  "flex",
  "flex-end",
  "flex-start",
  "footnotes",
  "forwards",
  "from",
  "geometricPrecision",
  "graytext",
  "grid",
  "groove",
  "hand",
  "hard-light",
  "help",
  "hidden",
  "hide",
  "higher",
  "highlight",
  "highlighttext",
  "horizontal",
  "hsl",
  "hsla",
  "hue",
  "icon",
  "ignore",
  "inactiveborder",
  "inactivecaption",
  "inactivecaptiontext",
  "infinite",
  "infobackground",
  "infotext",
  "inherit",
  "initial",
  "inline",
  "inline-axis",
  "inline-block",
  "inline-flex",
  "inline-grid",
  "inline-table",
  "inset",
  "inside",
  "intrinsic",
  "invert",
  "italic",
  "justify",
  "keep-all",
  "landscape",
  "large",
  "larger",
  "left",
  "level",
  "lighter",
  "lighten",
  "line-through",
  "linear",
  "linear-gradient",
  "lines",
  "list-item",
  "listbox",
  "listitem",
  "local",
  "logical",
  "loud",
  "lower",
  "lower-hexadecimal",
  "lower-latin",
  "lower-norwegian",
  "lowercase",
  "ltr",
  "luminosity",
  "manipulation",
  "match",
  "matrix",
  "matrix3d",
  "medium",
  "menu",
  "menutext",
  "message-box",
  "middle",
  "min-intrinsic",
  "mix",
  "monospace",
  "move",
  "multiple",
  "multiple_mask_images",
  "multiply",
  "n-resize",
  "narrower",
  "ne-resize",
  "nesw-resize",
  "no-close-quote",
  "no-drop",
  "no-open-quote",
  "no-repeat",
  "none",
  "normal",
  "not-allowed",
  "nowrap",
  "ns-resize",
  "numbers",
  "numeric",
  "nw-resize",
  "nwse-resize",
  "oblique",
  "opacity",
  "open-quote",
  "optimizeLegibility",
  "optimizeSpeed",
  "outset",
  "outside",
  "outside-shape",
  "overlay",
  "overline",
  "padding",
  "padding-box",
  "painted",
  "page",
  "paused",
  "perspective",
  "pinch-zoom",
  "plus-darker",
  "plus-lighter",
  "pointer",
  "polygon",
  "portrait",
  "pre",
  "pre-line",
  "pre-wrap",
  "preserve-3d",
  "progress",
  "push-button",
  "radial-gradient",
  "radio",
  "read-only",
  "read-write",
  "read-write-plaintext-only",
  "rectangle",
  "region",
  "relative",
  "repeat",
  "repeating-linear-gradient",
  "repeating-radial-gradient",
  "repeat-x",
  "repeat-y",
  "reset",
  "reverse",
  "rgb",
  "rgba",
  "ridge",
  "right",
  "rotate",
  "rotate3d",
  "rotateX",
  "rotateY",
  "rotateZ",
  "round",
  "row",
  "row-resize",
  "row-reverse",
  "rtl",
  "run-in",
  "running",
  "s-resize",
  "sans-serif",
  "saturation",
  "scale",
  "scale3d",
  "scaleX",
  "scaleY",
  "scaleZ",
  "screen",
  "scroll",
  "scrollbar",
  "scroll-position",
  "se-resize",
  "self-start",
  "self-end",
  "semi-condensed",
  "semi-expanded",
  "separate",
  "serif",
  "show",
  "single",
  "skew",
  "skewX",
  "skewY",
  "skip-white-space",
  "slide",
  "slider-horizontal",
  "slider-vertical",
  "sliderthumb-horizontal",
  "sliderthumb-vertical",
  "slow",
  "small",
  "small-caps",
  "small-caption",
  "smaller",
  "soft-light",
  "solid",
  "source-atop",
  "source-in",
  "source-out",
  "source-over",
  "space",
  "space-around",
  "space-between",
  "space-evenly",
  "spell-out",
  "square",
  "start",
  "static",
  "status-bar",
  "stretch",
  "stroke",
  "stroke-box",
  "sub",
  "subpixel-antialiased",
  "svg_masks",
  "super",
  "sw-resize",
  "symbolic",
  "symbols",
  "system-ui",
  "table",
  "table-caption",
  "table-cell",
  "table-column",
  "table-column-group",
  "table-footer-group",
  "table-header-group",
  "table-row",
  "table-row-group",
  "text",
  "text-bottom",
  "text-top",
  "textarea",
  "textfield",
  "thick",
  "thin",
  "threeddarkshadow",
  "threedface",
  "threedhighlight",
  "threedlightshadow",
  "threedshadow",
  "to",
  "top",
  "transform",
  "translate",
  "translate3d",
  "translateX",
  "translateY",
  "translateZ",
  "transparent",
  "ultra-condensed",
  "ultra-expanded",
  "underline",
  "unidirectional-pan",
  "unset",
  "up",
  "upper-latin",
  "uppercase",
  "url",
  "var",
  "vertical",
  "vertical-text",
  "view-box",
  "visible",
  "visibleFill",
  "visiblePainted",
  "visibleStroke",
  "visual",
  "w-resize",
  "wait",
  "wave",
  "wider",
  "window",
  "windowframe",
  "windowtext",
  "words",
  "wrap",
  "wrap-reverse",
  "x-large",
  "x-small",
  "xor",
  "xx-large",
  "xx-small"
].map((name) => ({ type: "keyword", label: name })).concat(/* @__PURE__ */ [
  "aliceblue",
  "antiquewhite",
  "aqua",
  "aquamarine",
  "azure",
  "beige",
  "bisque",
  "black",
  "blanchedalmond",
  "blue",
  "blueviolet",
  "brown",
  "burlywood",
  "cadetblue",
  "chartreuse",
  "chocolate",
  "coral",
  "cornflowerblue",
  "cornsilk",
  "crimson",
  "cyan",
  "darkblue",
  "darkcyan",
  "darkgoldenrod",
  "darkgray",
  "darkgreen",
  "darkkhaki",
  "darkmagenta",
  "darkolivegreen",
  "darkorange",
  "darkorchid",
  "darkred",
  "darksalmon",
  "darkseagreen",
  "darkslateblue",
  "darkslategray",
  "darkturquoise",
  "darkviolet",
  "deeppink",
  "deepskyblue",
  "dimgray",
  "dodgerblue",
  "firebrick",
  "floralwhite",
  "forestgreen",
  "fuchsia",
  "gainsboro",
  "ghostwhite",
  "gold",
  "goldenrod",
  "gray",
  "grey",
  "green",
  "greenyellow",
  "honeydew",
  "hotpink",
  "indianred",
  "indigo",
  "ivory",
  "khaki",
  "lavender",
  "lavenderblush",
  "lawngreen",
  "lemonchiffon",
  "lightblue",
  "lightcoral",
  "lightcyan",
  "lightgoldenrodyellow",
  "lightgray",
  "lightgreen",
  "lightpink",
  "lightsalmon",
  "lightseagreen",
  "lightskyblue",
  "lightslategray",
  "lightsteelblue",
  "lightyellow",
  "lime",
  "limegreen",
  "linen",
  "magenta",
  "maroon",
  "mediumaquamarine",
  "mediumblue",
  "mediumorchid",
  "mediumpurple",
  "mediumseagreen",
  "mediumslateblue",
  "mediumspringgreen",
  "mediumturquoise",
  "mediumvioletred",
  "midnightblue",
  "mintcream",
  "mistyrose",
  "moccasin",
  "navajowhite",
  "navy",
  "oldlace",
  "olive",
  "olivedrab",
  "orange",
  "orangered",
  "orchid",
  "palegoldenrod",
  "palegreen",
  "paleturquoise",
  "palevioletred",
  "papayawhip",
  "peachpuff",
  "peru",
  "pink",
  "plum",
  "powderblue",
  "purple",
  "rebeccapurple",
  "red",
  "rosybrown",
  "royalblue",
  "saddlebrown",
  "salmon",
  "sandybrown",
  "seagreen",
  "seashell",
  "sienna",
  "silver",
  "skyblue",
  "slateblue",
  "slategray",
  "snow",
  "springgreen",
  "steelblue",
  "tan",
  "teal",
  "thistle",
  "tomato",
  "turquoise",
  "violet",
  "wheat",
  "white",
  "whitesmoke",
  "yellow",
  "yellowgreen"
].map((name) => ({ type: "constant", label: name })));
const tags = /* @__PURE__ */ [
  "a",
  "abbr",
  "address",
  "article",
  "aside",
  "b",
  "bdi",
  "bdo",
  "blockquote",
  "body",
  "br",
  "button",
  "canvas",
  "caption",
  "cite",
  "code",
  "col",
  "colgroup",
  "dd",
  "del",
  "details",
  "dfn",
  "dialog",
  "div",
  "dl",
  "dt",
  "em",
  "figcaption",
  "figure",
  "footer",
  "form",
  "header",
  "hgroup",
  "h1",
  "h2",
  "h3",
  "h4",
  "h5",
  "h6",
  "hr",
  "html",
  "i",
  "iframe",
  "img",
  "input",
  "ins",
  "kbd",
  "label",
  "legend",
  "li",
  "main",
  "meter",
  "nav",
  "ol",
  "output",
  "p",
  "pre",
  "ruby",
  "section",
  "select",
  "small",
  "source",
  "span",
  "strong",
  "sub",
  "summary",
  "sup",
  "table",
  "tbody",
  "td",
  "template",
  "textarea",
  "tfoot",
  "th",
  "thead",
  "tr",
  "u",
  "ul"
].map((name) => ({ type: "type", label: name }));
const identifier = /^(\w[\w-]*|-\w[\w-]*|)$/, variable = /^-(-[\w-]*)?$/;
function isVarArg(node, doc) {
  var _a;
  if (node.name == "(" || node.type.isError)
    node = node.parent || node;
  if (node.name != "ArgList")
    return false;
  let callee2 = (_a = node.parent) === null || _a === void 0 ? void 0 : _a.firstChild;
  if ((callee2 === null || callee2 === void 0 ? void 0 : callee2.name) != "Callee")
    return false;
  return doc.sliceString(callee2.from, callee2.to) == "var";
}
const VariablesByNode = /* @__PURE__ */ new NodeWeakMap();
const declSelector = ["Declaration"];
function variableNames(doc, node) {
  if (node.to - node.from > 4096) {
    let known = VariablesByNode.get(node);
    if (known)
      return known;
    let result = [], seen = /* @__PURE__ */ new Set(), cursor = node.cursor(IterMode.IncludeAnonymous);
    if (cursor.firstChild())
      do {
        for (let option of variableNames(doc, cursor.node))
          if (!seen.has(option.label)) {
            seen.add(option.label);
            result.push(option);
          }
      } while (cursor.nextSibling());
    VariablesByNode.set(node, result);
    return result;
  } else {
    let result = [], seen = /* @__PURE__ */ new Set();
    node.cursor().iterate((node2) => {
      var _a;
      if (node2.name == "VariableName" && node2.matchContext(declSelector) && ((_a = node2.node.nextSibling) === null || _a === void 0 ? void 0 : _a.name) == ":") {
        let name = doc.sliceString(node2.from, node2.to);
        if (!seen.has(name)) {
          seen.add(name);
          result.push({ label: name, type: "variable" });
        }
      }
    });
    return result;
  }
}
const cssCompletionSource = (context) => {
  var _a;
  let { state, pos } = context, node = syntaxTree(state).resolveInner(pos, -1);
  let isDash = node.type.isError && node.from == node.to - 1 && state.doc.sliceString(node.from, node.to) == "-";
  if (node.name == "PropertyName" || isDash && ((_a = node.parent) === null || _a === void 0 ? void 0 : _a.name) == "Block")
    return { from: node.from, options: properties(), validFor: identifier };
  if (node.name == "ValueName")
    return { from: node.from, options: values, validFor: identifier };
  if (node.name == "PseudoClassName")
    return { from: node.from, options: pseudoClasses, validFor: identifier };
  if (node.name == "VariableName" || (context.explicit || isDash) && isVarArg(node, state.doc))
    return {
      from: node.name == "VariableName" ? node.from : pos,
      options: variableNames(state.doc, syntaxTree(state).topNode),
      validFor: variable
    };
  if (node.name == "TagName") {
    for (let { parent } = node; parent; parent = parent.parent)
      if (parent.name == "Block")
        return { from: node.from, options: properties(), validFor: identifier };
    return { from: node.from, options: tags, validFor: identifier };
  }
  if (!context.explicit)
    return null;
  let above = node.resolve(pos), before = above.childBefore(pos);
  if (before && before.name == ":" && above.name == "PseudoClassSelector")
    return { from: pos, options: pseudoClasses, validFor: identifier };
  if (before && before.name == ":" && above.name == "Declaration" || above.name == "ArgList")
    return { from: pos, options: values, validFor: identifier };
  if (above.name == "Block")
    return { from: pos, options: properties(), validFor: identifier };
  return null;
};
const cssLanguage = /* @__PURE__ */ LRLanguage.define({
  name: "css",
  parser: /* @__PURE__ */ parser.configure({
    props: [
      /* @__PURE__ */ indentNodeProp.add({
        Declaration: /* @__PURE__ */ continuedIndent()
      }),
      /* @__PURE__ */ foldNodeProp.add({
        Block: foldInside
      })
    ]
  }),
  languageData: {
    commentTokens: { block: { open: "/*", close: "*/" } },
    indentOnInput: /^\s*\}$/,
    wordChars: "-"
  }
});
function css() {
  return new LanguageSupport(cssLanguage, cssLanguage.data.of({ autocomplete: cssCompletionSource }));
}

export { css, cssCompletionSource, cssLanguage };
//# sourceMappingURL=index34-BoaxPsGz.js.map
