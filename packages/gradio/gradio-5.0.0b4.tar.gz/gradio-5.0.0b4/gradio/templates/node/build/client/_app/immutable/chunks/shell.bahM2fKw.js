var c={};function s(n,e){for(var r=0;r<e.length;r++)c[e[r]]=n}var k=["true","false"],h=["if","then","do","else","elif","while","until","for","in","esac","fi","fin","fil","done","exit","set","unset","export","function"],p=["ab","awk","bash","beep","cat","cc","cd","chown","chmod","chroot","clear","cp","curl","cut","diff","echo","find","gawk","gcc","get","git","grep","hg","kill","killall","ln","ls","make","mkdir","openssl","mv","nc","nl","node","npm","ping","ps","restart","rm","rmdir","sed","service","sh","shopt","shred","source","sort","sleep","ssh","start","stop","su","sudo","svn","tee","telnet","top","touch","vi","vim","wall","wc","wget","who","write","yes","zsh"];s("atom",k);s("keyword",h);s("builtin",p);function d(n,e){if(n.eatSpace())return null;var r=n.sol(),t=n.next();if(t==="\\")return n.next(),null;if(t==="'"||t==='"'||t==="`")return e.tokens.unshift(l(t,t==="`"?"quote":"string")),u(n,e);if(t==="#")return r&&n.eat("!")?(n.skipToEnd(),"meta"):(n.skipToEnd(),"comment");if(t==="$")return e.tokens.unshift(a),u(n,e);if(t==="+"||t==="=")return"operator";if(t==="-")return n.eat("-"),n.eatWhile(/\w/),"attribute";if(t=="<"){if(n.match("<<"))return"operator";var o=n.match(/^<-?\s*['"]?([^'"]*)['"]?/);if(o)return e.tokens.unshift(w(o[1])),"string.special"}if(/\d/.test(t)&&(n.eatWhile(/\d/),n.eol()||!/\w/.test(n.peek())))return"number";n.eatWhile(/[\w-]/);var i=n.current();return n.peek()==="="&&/\w+/.test(i)?"def":c.hasOwnProperty(i)?c[i]:null}function l(n,e){var r=n=="("?")":n=="{"?"}":n;return function(t,o){for(var i,f=!1;(i=t.next())!=null;){if(i===r&&!f){o.tokens.shift();break}else if(i==="$"&&!f&&n!=="'"&&t.peek()!=r){f=!0,t.backUp(1),o.tokens.unshift(a);break}else{if(!f&&n!==r&&i===n)return o.tokens.unshift(l(n,e)),u(t,o);if(!f&&/['"]/.test(i)&&!/['"]/.test(n)){o.tokens.unshift(g(i,"string")),t.backUp(1);break}}f=!f&&i==="\\"}return e}}function g(n,e){return function(r,t){return t.tokens[0]=l(n,e),r.next(),u(r,t)}}var a=function(n,e){e.tokens.length>1&&n.eat("$");var r=n.next();return/['"({]/.test(r)?(e.tokens[0]=l(r,r=="("?"quote":r=="{"?"def":"string"),u(n,e)):(/\d/.test(r)||n.eatWhile(/\w/),e.tokens.shift(),"def")};function w(n){return function(e,r){return e.sol()&&e.string==n&&r.tokens.shift(),e.skipToEnd(),"string.special"}}function u(n,e){return(e.tokens[0]||d)(n,e)}const v={name:"shell",startState:function(){return{tokens:[]}},token:function(n,e){return u(n,e)},languageData:{autocomplete:k.concat(h,p),closeBrackets:{brackets:["(","[","{","'",'"',"`"]},commentTokens:{line:"#"}}};export{v as shell};
