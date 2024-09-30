import{s as de,r as X,a as F,e as Y,g as G,c as Z,b as y,f as z,p as H,i as E,h as fe,L as $,y as Fe,M as q,t as ce,d as me,j as ge,n as he,z as x,l as Ge,u as He,m as Qe,o as Re,K as w,B as ve}from"./scheduler.xQsDa6L3.js";import{S as ke,i as pe,f as ee,c as B,a as I,m as S,g as le,b as k,e as ne,t as p,d as j}from"./index.lnKugwF0.js";import{U as Xe}from"./Upload.d4auggP1.js";import{B as ze,d as Ve,b as Be,e as Ie}from"./2.Bbgn9Xo5.js";import{B as Ye}from"./BlockLabel.EPnqKJ7A.js";import{V as Ze}from"./Video.erEfpUh6.js";import{S as ye}from"./SelectSource.Bi7MVZmg.js";/* empty css                                                   */import"./Image.BHfoMI0G.js";/* empty css                                                   */import{W as $e}from"./ImageUploader.DfCVz4tI.js";/* empty css                                              */import{p as be,a as xe}from"./Video.BpynpsrS.js";import{l as Kl}from"./Video.BpynpsrS.js";import{P as el,V as ll}from"./VideoPreview.rbSYfVYJ.js";import{default as Tl}from"./Example.BPq4ao6I.js";import{U as nl}from"./UploadText.sHqbxECQ.js";function tl(n){let e,t=(n[0].orig_name||n[0].url)+"",l,a,i,o=be(n[0].size)+"",r;return{c(){e=Y("div"),l=ce(t),a=F(),i=Y("div"),r=ce(o),this.h()},l(s){e=Z(s,"DIV",{class:!0});var h=y(e);l=me(h,t),h.forEach(z),a=G(s),i=Z(s,"DIV",{class:!0});var u=y(i);r=me(u,o),u.forEach(z),this.h()},h(){H(e,"class","file-name svelte-1kyjvp4"),H(i,"class","file-size svelte-1kyjvp4")},m(s,h){E(s,e,h),fe(e,l),E(s,a,h),E(s,i,h),fe(i,r)},p(s,h){h[0]&1&&t!==(t=(s[0].orig_name||s[0].url)+"")&&ge(l,t),h[0]&1&&o!==(o=be(s[0].size)+"")&&ge(r,o)},i:he,o:he,d(s){s&&(z(e),z(a),z(i))}}}function al(n){var i;let e=(i=n[0])==null?void 0:i.url,t,l,a=we(n);return{c(){a.c(),t=x()},l(o){a.l(o),t=x()},m(o,r){a.m(o,r),E(o,t,r),l=!0},p(o,r){var s;r[0]&1&&de(e,e=(s=o[0])==null?void 0:s.url)?(le(),k(a,1,1,he),ne(),a=we(o),a.c(),p(a,1),a.m(t.parentNode,t)):a.p(o,r)},i(o){l||(p(a),l=!0)},o(o){k(a),l=!1},d(o){o&&z(t),a.d(o)}}}function il(n){let e,t,l,a;const i=[ol,sl],o=[];function r(s,h){return s[1]==="upload"?0:s[1]==="webcam"?1:-1}return~(t=r(n))&&(l=o[t]=i[t](n)),{c(){e=Y("div"),l&&l.c(),this.h()},l(s){e=Z(s,"DIV",{class:!0});var h=y(e);l&&l.l(h),h.forEach(z),this.h()},h(){H(e,"class","upload-container svelte-1kyjvp4")},m(s,h){E(s,e,h),~t&&o[t].m(e,null),a=!0},p(s,h){let u=t;t=r(s),t===u?~t&&o[t].p(s,h):(l&&(le(),k(o[u],1,1,()=>{o[u]=null}),ne()),~t?(l=o[t],l?l.p(s,h):(l=o[t]=i[t](s),l.c()),p(l,1),l.m(e,null)):l=null)},i(s){a||(p(l),a=!0)},o(s){k(l),a=!1},d(s){s&&z(e),~t&&o[t].d()}}}function we(n){var l;let e,t;return e=new el({props:{upload:n[15],root:n[11],interactive:!0,autoplay:n[10],src:n[0].url,subtitle:(l=n[3])==null?void 0:l.url,is_stream:!1,mirror:n[8]&&n[1]==="webcam",label:n[5],handle_change:n[23],handle_reset_value:n[13],loop:n[17],value:n[0],i18n:n[12],show_download_button:n[6],handle_clear:n[22],has_change_history:n[19]}}),e.$on("play",n[32]),e.$on("pause",n[33]),e.$on("stop",n[34]),e.$on("end",n[35]),{c(){B(e.$$.fragment)},l(a){I(e.$$.fragment,a)},m(a,i){S(e,a,i),t=!0},p(a,i){var r;const o={};i[0]&32768&&(o.upload=a[15]),i[0]&2048&&(o.root=a[11]),i[0]&1024&&(o.autoplay=a[10]),i[0]&1&&(o.src=a[0].url),i[0]&8&&(o.subtitle=(r=a[3])==null?void 0:r.url),i[0]&258&&(o.mirror=a[8]&&a[1]==="webcam"),i[0]&32&&(o.label=a[5]),i[0]&8192&&(o.handle_reset_value=a[13]),i[0]&131072&&(o.loop=a[17]),i[0]&1&&(o.value=a[0]),i[0]&4096&&(o.i18n=a[12]),i[0]&64&&(o.show_download_button=a[6]),i[0]&524288&&(o.has_change_history=a[19]),e.$set(o)},i(a){t||(p(e.$$.fragment,a),t=!0)},o(a){k(e.$$.fragment,a),t=!1},d(a){j(e,a)}}}function sl(n){let e,t;return e=new $e({props:{root:n[11],mirror_webcam:n[8],include_audio:n[9],mode:"video",i18n:n[12],upload:n[15],stream_every:1}}),e.$on("error",n[29]),e.$on("capture",n[24]),e.$on("start_recording",n[30]),e.$on("stop_recording",n[31]),{c(){B(e.$$.fragment)},l(l){I(e.$$.fragment,l)},m(l,a){S(e,l,a),t=!0},p(l,a){const i={};a[0]&2048&&(i.root=l[11]),a[0]&256&&(i.mirror_webcam=l[8]),a[0]&512&&(i.include_audio=l[9]),a[0]&4096&&(i.i18n=l[12]),a[0]&32768&&(i.upload=l[15]),e.$set(i)},i(l){t||(p(e.$$.fragment,l),t=!0)},o(l){k(e.$$.fragment,l),t=!1},d(l){j(e,l)}}}function ol(n){let e,t,l,a;function i(s){n[26](s)}function o(s){n[27](s)}let r={filetype:"video/x-m4v,video/*",max_file_size:n[14],root:n[11],upload:n[15],stream_handler:n[16],$$slots:{default:[ul]},$$scope:{ctx:n}};return n[18]!==void 0&&(r.dragging=n[18]),n[2]!==void 0&&(r.uploading=n[2]),e=new Xe({props:r}),X.push(()=>ee(e,"dragging",i)),X.push(()=>ee(e,"uploading",o)),e.$on("load",n[21]),e.$on("error",n[28]),{c(){B(e.$$.fragment)},l(s){I(e.$$.fragment,s)},m(s,h){S(e,s,h),a=!0},p(s,h){const u={};h[0]&16384&&(u.max_file_size=s[14]),h[0]&2048&&(u.root=s[11]),h[0]&32768&&(u.upload=s[15]),h[0]&65536&&(u.stream_handler=s[16]),h[1]&64&&(u.$$scope={dirty:h,ctx:s}),!t&&h[0]&262144&&(t=!0,u.dragging=s[18],$(()=>t=!1)),!l&&h[0]&4&&(l=!0,u.uploading=s[2],$(()=>l=!1)),e.$set(u)},i(s){a||(p(e.$$.fragment,s),a=!0)},o(s){k(e.$$.fragment,s),a=!1},d(s){j(e,s)}}}function ul(n){let e;const t=n[25].default,l=Ge(t,n,n[37],null);return{c(){l&&l.c()},l(a){l&&l.l(a)},m(a,i){l&&l.m(a,i),e=!0},p(a,i){l&&l.p&&(!e||i[1]&64)&&He(l,t,a,a[37],e?Re(t,a[37],i,null):Qe(a[37]),null)},i(a){e||(p(l,a),e=!0)},o(a){k(l,a),e=!1},d(a){l&&l.d(a)}}}function rl(n){let e,t,l,a,i,o,r,s,h,u;e=new Ye({props:{show_label:n[7],Icon:Ze,label:n[5]||"Video"}});const c=[il,al,tl],b=[];function m(d,v){return d[0]===null||d[0].url===void 0?0:(a==null&&(a=!!xe()),a?1:d[0].size?2:-1)}~(i=m(n))&&(o=b[i]=c[i](n));function O(d){n[36](d)}let U={sources:n[4],handle_clear:n[22]};return n[1]!==void 0&&(U.active_source=n[1]),s=new ye({props:U}),X.push(()=>ee(s,"active_source",O)),{c(){B(e.$$.fragment),t=F(),l=Y("div"),o&&o.c(),r=F(),B(s.$$.fragment),this.h()},l(d){I(e.$$.fragment,d),t=G(d),l=Z(d,"DIV",{"data-testid":!0,class:!0});var v=y(l);o&&o.l(v),r=G(v),I(s.$$.fragment,v),v.forEach(z),this.h()},h(){H(l,"data-testid","video"),H(l,"class","video-container svelte-1kyjvp4")},m(d,v){S(e,d,v),E(d,t,v),E(d,l,v),~i&&b[i].m(l,null),fe(l,r),S(s,l,null),u=!0},p(d,v){const D={};v[0]&128&&(D.show_label=d[7]),v[0]&32&&(D.label=d[5]||"Video"),e.$set(D);let N=i;i=m(d),i===N?~i&&b[i].p(d,v):(o&&(le(),k(b[N],1,1,()=>{b[N]=null}),ne()),~i?(o=b[i],o?o.p(d,v):(o=b[i]=c[i](d),o.c()),p(o,1),o.m(l,r)):o=null);const P={};v[0]&16&&(P.sources=d[4]),!h&&v[0]&2&&(h=!0,P.active_source=d[1],$(()=>h=!1)),s.$set(P)},i(d){u||(p(e.$$.fragment,d),p(o),p(s.$$.fragment,d),u=!0)},o(d){k(e.$$.fragment,d),k(o),k(s.$$.fragment,d),u=!1},d(d){d&&(z(t),z(l)),j(e,d),~i&&b[i].d(),j(s)}}}function _l(n,e,t){let{$$slots:l={},$$scope:a}=e,{value:i=null}=e,{subtitle:o=null}=e,{sources:r=["webcam","upload"]}=e,{label:s=void 0}=e,{show_download_button:h=!1}=e,{show_label:u=!0}=e,{mirror_webcam:c=!1}=e,{include_audio:b}=e,{autoplay:m}=e,{root:O}=e,{i18n:U}=e,{active_source:d="webcam"}=e,{handle_reset_value:v=()=>{}}=e,{max_file_size:D=null}=e,{upload:N}=e,{stream_handler:P}=e,{loop:g}=e,{uploading:W=!1}=e,K=!1;const V=Fe();function Q({detail:_}){t(0,i=_),V("change",_),V("upload",_)}function M(){t(0,i=null),V("change",null),V("clear")}function C(_){t(19,K=!0),V("change",_)}function T({detail:_}){V("change",_)}let J=!1;function A(_){J=_,t(18,J)}function L(_){W=_,t(2,W)}const te=({detail:_})=>V("error",_);function R(_){q.call(this,n,_)}function ae(_){q.call(this,n,_)}function ie(_){q.call(this,n,_)}function se(_){q.call(this,n,_)}function oe(_){q.call(this,n,_)}function ue(_){q.call(this,n,_)}function re(_){q.call(this,n,_)}function _e(_){d=_,t(1,d)}return n.$$set=_=>{"value"in _&&t(0,i=_.value),"subtitle"in _&&t(3,o=_.subtitle),"sources"in _&&t(4,r=_.sources),"label"in _&&t(5,s=_.label),"show_download_button"in _&&t(6,h=_.show_download_button),"show_label"in _&&t(7,u=_.show_label),"mirror_webcam"in _&&t(8,c=_.mirror_webcam),"include_audio"in _&&t(9,b=_.include_audio),"autoplay"in _&&t(10,m=_.autoplay),"root"in _&&t(11,O=_.root),"i18n"in _&&t(12,U=_.i18n),"active_source"in _&&t(1,d=_.active_source),"handle_reset_value"in _&&t(13,v=_.handle_reset_value),"max_file_size"in _&&t(14,D=_.max_file_size),"upload"in _&&t(15,N=_.upload),"stream_handler"in _&&t(16,P=_.stream_handler),"loop"in _&&t(17,g=_.loop),"uploading"in _&&t(2,W=_.uploading),"$$scope"in _&&t(37,a=_.$$scope)},n.$$.update=()=>{n.$$.dirty[0]&262144&&V("drag",J)},[i,d,W,o,r,s,h,u,c,b,m,O,U,v,D,N,P,g,J,K,V,Q,M,C,T,l,A,L,te,R,ae,ie,se,oe,ue,re,_e,a]}class fl extends ke{constructor(e){super(),pe(this,e,_l,rl,de,{value:0,subtitle:3,sources:4,label:5,show_download_button:6,show_label:7,mirror_webcam:8,include_audio:9,autoplay:10,root:11,i18n:12,active_source:1,handle_reset_value:13,max_file_size:14,upload:15,stream_handler:16,loop:17,uploading:2},null,[-1,-1])}}const hl=fl;function dl(n){let e,t;return e=new ze({props:{visible:n[4],variant:n[0]===null&&n[23]==="upload"?"dashed":"solid",border_mode:n[26]?"focus":"base",padding:!1,elem_id:n[2],elem_classes:n[3],height:n[9],width:n[10],container:n[11],scale:n[12],min_width:n[13],allow_overflow:!1,$$slots:{default:[gl]},$$scope:{ctx:n}}}),{c(){B(e.$$.fragment)},l(l){I(e.$$.fragment,l)},m(l,a){S(e,l,a),t=!0},p(l,a){const i={};a[0]&16&&(i.visible=l[4]),a[0]&8388609&&(i.variant=l[0]===null&&l[23]==="upload"?"dashed":"solid"),a[0]&67108864&&(i.border_mode=l[26]?"focus":"base"),a[0]&4&&(i.elem_id=l[2]),a[0]&8&&(i.elem_classes=l[3]),a[0]&512&&(i.height=l[9]),a[0]&1024&&(i.width=l[10]),a[0]&2048&&(i.container=l[11]),a[0]&4096&&(i.scale=l[12]),a[0]&8192&&(i.min_width=l[13]),a[0]&133906914|a[1]&8388608&&(i.$$scope={dirty:a,ctx:l}),e.$set(i)},i(l){t||(p(e.$$.fragment,l),t=!0)},o(l){k(e.$$.fragment,l),t=!1},d(l){j(e,l)}}}function cl(n){let e,t;return e=new ze({props:{visible:n[4],variant:n[0]===null&&n[23]==="upload"?"dashed":"solid",border_mode:n[26]?"focus":"base",padding:!1,elem_id:n[2],elem_classes:n[3],height:n[9],width:n[10],container:n[11],scale:n[12],min_width:n[13],allow_overflow:!1,$$slots:{default:[bl]},$$scope:{ctx:n}}}),{c(){B(e.$$.fragment)},l(l){I(e.$$.fragment,l)},m(l,a){S(e,l,a),t=!0},p(l,a){const i={};a[0]&16&&(i.visible=l[4]),a[0]&8388609&&(i.variant=l[0]===null&&l[23]==="upload"?"dashed":"solid"),a[0]&67108864&&(i.border_mode=l[26]?"focus":"base"),a[0]&4&&(i.elem_id=l[2]),a[0]&8&&(i.elem_classes=l[3]),a[0]&512&&(i.height=l[9]),a[0]&1024&&(i.width=l[10]),a[0]&2048&&(i.container=l[11]),a[0]&4096&&(i.scale=l[12]),a[0]&8192&&(i.min_width=l[13]),a[0]&52674850|a[1]&8388608&&(i.$$scope={dirty:a,ctx:l}),e.$set(i)},i(l){t||(p(e.$$.fragment,l),t=!0)},o(l){k(e.$$.fragment,l),t=!1},d(l){j(e,l)}}}function ml(n){let e,t;return e=new nl({props:{i18n:n[17].i18n,type:"video"}}),{c(){B(e.$$.fragment)},l(l){I(e.$$.fragment,l)},m(l,a){S(e,l,a),t=!0},p(l,a){const i={};a[0]&131072&&(i.i18n=l[17].i18n),e.$set(i)},i(l){t||(p(e.$$.fragment,l),t=!0)},o(l){k(e.$$.fragment,l),t=!1},d(l){j(e,l)}}}function gl(n){let e,t,l,a,i;const o=[{autoscroll:n[17].autoscroll},{i18n:n[17].i18n},n[1]];let r={};for(let u=0;u<o.length;u+=1)r=ve(r,o[u]);e=new Ve({props:r}),e.$on("clear_status",n[41]);function s(u){n[44](u)}let h={value:n[24],subtitle:n[25],label:n[5],show_label:n[8],show_download_button:n[16],sources:n[6],active_source:n[23],mirror_webcam:n[19],include_audio:n[20],autoplay:n[14],root:n[7],loop:n[21],handle_reset_value:n[27],i18n:n[17].i18n,max_file_size:n[17].max_file_size,upload:n[42],stream_handler:n[43],$$slots:{default:[ml]},$$scope:{ctx:n}};return n[22]!==void 0&&(h.uploading=n[22]),l=new hl({props:h}),X.push(()=>ee(l,"uploading",s)),l.$on("change",n[28]),l.$on("drag",n[45]),l.$on("error",n[29]),l.$on("clear",n[46]),l.$on("play",n[47]),l.$on("pause",n[48]),l.$on("upload",n[49]),l.$on("stop",n[50]),l.$on("end",n[51]),l.$on("start_recording",n[52]),l.$on("stop_recording",n[53]),{c(){B(e.$$.fragment),t=F(),B(l.$$.fragment)},l(u){I(e.$$.fragment,u),t=G(u),I(l.$$.fragment,u)},m(u,c){S(e,u,c),E(u,t,c),S(l,u,c),i=!0},p(u,c){const b=c[0]&131074?Be(o,[c[0]&131072&&{autoscroll:u[17].autoscroll},c[0]&131072&&{i18n:u[17].i18n},c[0]&2&&Ie(u[1])]):{};e.$set(b);const m={};c[0]&16777216&&(m.value=u[24]),c[0]&33554432&&(m.subtitle=u[25]),c[0]&32&&(m.label=u[5]),c[0]&256&&(m.show_label=u[8]),c[0]&65536&&(m.show_download_button=u[16]),c[0]&64&&(m.sources=u[6]),c[0]&8388608&&(m.active_source=u[23]),c[0]&524288&&(m.mirror_webcam=u[19]),c[0]&1048576&&(m.include_audio=u[20]),c[0]&16384&&(m.autoplay=u[14]),c[0]&128&&(m.root=u[7]),c[0]&2097152&&(m.loop=u[21]),c[0]&131072&&(m.i18n=u[17].i18n),c[0]&131072&&(m.max_file_size=u[17].max_file_size),c[0]&131072&&(m.upload=u[42]),c[0]&131072&&(m.stream_handler=u[43]),c[0]&131072|c[1]&8388608&&(m.$$scope={dirty:c,ctx:u}),!a&&c[0]&4194304&&(a=!0,m.uploading=u[22],$(()=>a=!1)),l.$set(m)},i(u){i||(p(e.$$.fragment,u),p(l.$$.fragment,u),i=!0)},o(u){k(e.$$.fragment,u),k(l.$$.fragment,u),i=!1},d(u){u&&z(t),j(e,u),j(l,u)}}}function bl(n){let e,t,l,a;const i=[{autoscroll:n[17].autoscroll},{i18n:n[17].i18n},n[1]];let o={};for(let r=0;r<i.length;r+=1)o=ve(o,i[r]);return e=new Ve({props:o}),e.$on("clear_status",n[33]),l=new ll({props:{value:n[24],subtitle:n[25],label:n[5],show_label:n[8],autoplay:n[14],loop:n[21],show_share_button:n[15],show_download_button:n[16],i18n:n[17].i18n,upload:n[34]}}),l.$on("play",n[35]),l.$on("pause",n[36]),l.$on("stop",n[37]),l.$on("end",n[38]),l.$on("share",n[39]),l.$on("error",n[40]),{c(){B(e.$$.fragment),t=F(),B(l.$$.fragment)},l(r){I(e.$$.fragment,r),t=G(r),I(l.$$.fragment,r)},m(r,s){S(e,r,s),E(r,t,s),S(l,r,s),a=!0},p(r,s){const h=s[0]&131074?Be(i,[s[0]&131072&&{autoscroll:r[17].autoscroll},s[0]&131072&&{i18n:r[17].i18n},s[0]&2&&Ie(r[1])]):{};e.$set(h);const u={};s[0]&16777216&&(u.value=r[24]),s[0]&33554432&&(u.subtitle=r[25]),s[0]&32&&(u.label=r[5]),s[0]&256&&(u.show_label=r[8]),s[0]&16384&&(u.autoplay=r[14]),s[0]&2097152&&(u.loop=r[21]),s[0]&32768&&(u.show_share_button=r[15]),s[0]&65536&&(u.show_download_button=r[16]),s[0]&131072&&(u.i18n=r[17].i18n),s[0]&131072&&(u.upload=r[34]),l.$set(u)},i(r){a||(p(e.$$.fragment,r),p(l.$$.fragment,r),a=!0)},o(r){k(e.$$.fragment,r),k(l.$$.fragment,r),a=!1},d(r){r&&z(t),j(e,r),j(l,r)}}}function wl(n){let e,t,l,a;const i=[cl,dl],o=[];function r(s,h){return s[18]?1:0}return e=r(n),t=o[e]=i[e](n),{c(){t.c(),l=x()},l(s){t.l(s),l=x()},m(s,h){o[e].m(s,h),E(s,l,h),a=!0},p(s,h){let u=e;e=r(s),e===u?o[e].p(s,h):(le(),k(o[u],1,1,()=>{o[u]=null}),ne(),t=o[e],t?t.p(s,h):(t=o[e]=i[e](s),t.c()),p(t,1),t.m(l.parentNode,l))},i(s){a||(p(t),a=!0)},o(s){k(t),a=!1},d(s){s&&z(l),o[e].d(s)}}}function vl(n,e,t){let{elem_id:l=""}=e,{elem_classes:a=[]}=e,{visible:i=!0}=e,{value:o=null}=e,r=null,{label:s}=e,{sources:h}=e,{root:u}=e,{show_label:c}=e,{loading_status:b}=e,{height:m}=e,{width:O}=e,{container:U=!1}=e,{scale:d=null}=e,{min_width:v=void 0}=e,{autoplay:D=!1}=e,{show_share_button:N=!0}=e,{show_download_button:P}=e,{gradio:g}=e,{interactive:W}=e,{mirror_webcam:K}=e,{include_audio:V}=e,{loop:Q=!1}=e,{input_ready:M}=e,C=!1,T=null,J=null,A,L=o;const te=()=>{L===null||o===L||t(0,o=L)};let R=!1;function ae({detail:f}){f!=null?t(0,o={video:f,subtitles:null}):t(0,o=null)}function ie({detail:f}){const[Te,Ae]=f.includes("Invalid file type")?["warning","complete"]:["error","error"];t(1,b=b||{}),t(1,b.status=Ae,b),t(1,b.message=f,b),g.dispatch(Te,f)}const se=()=>g.dispatch("clear_status",b),oe=(...f)=>g.client.upload(...f),ue=()=>g.dispatch("play"),re=()=>g.dispatch("pause"),_e=()=>g.dispatch("stop"),_=()=>g.dispatch("end"),Se=({detail:f})=>g.dispatch("share",f),je=({detail:f})=>g.dispatch("error",f),Ee=()=>g.dispatch("clear_status",b),De=(...f)=>g.client.upload(...f),Ne=(...f)=>g.client.stream(...f);function Pe(f){C=f,t(22,C)}const Ue=({detail:f})=>t(26,R=f),Je=()=>g.dispatch("clear"),Le=()=>g.dispatch("play"),Oe=()=>g.dispatch("pause"),We=()=>g.dispatch("upload"),qe=()=>g.dispatch("stop"),Ce=()=>g.dispatch("end"),Ke=()=>g.dispatch("start_recording"),Me=()=>g.dispatch("stop_recording");return n.$$set=f=>{"elem_id"in f&&t(2,l=f.elem_id),"elem_classes"in f&&t(3,a=f.elem_classes),"visible"in f&&t(4,i=f.visible),"value"in f&&t(0,o=f.value),"label"in f&&t(5,s=f.label),"sources"in f&&t(6,h=f.sources),"root"in f&&t(7,u=f.root),"show_label"in f&&t(8,c=f.show_label),"loading_status"in f&&t(1,b=f.loading_status),"height"in f&&t(9,m=f.height),"width"in f&&t(10,O=f.width),"container"in f&&t(11,U=f.container),"scale"in f&&t(12,d=f.scale),"min_width"in f&&t(13,v=f.min_width),"autoplay"in f&&t(14,D=f.autoplay),"show_share_button"in f&&t(15,N=f.show_share_button),"show_download_button"in f&&t(16,P=f.show_download_button),"gradio"in f&&t(17,g=f.gradio),"interactive"in f&&t(18,W=f.interactive),"mirror_webcam"in f&&t(19,K=f.mirror_webcam),"include_audio"in f&&t(20,V=f.include_audio),"loop"in f&&t(21,Q=f.loop),"input_ready"in f&&t(30,M=f.input_ready)},n.$$.update=()=>{n.$$.dirty[0]&4194304&&t(30,M=!C),n.$$.dirty[0]&1|n.$$.dirty[1]&2&&o&&L===null&&t(32,L=o),n.$$.dirty[0]&8388672&&h&&!A&&t(23,A=h[0]),n.$$.dirty[0]&1&&(o!=null?(t(24,T=o.video),t(25,J=o.subtitles)):(t(24,T=null),t(25,J=null))),n.$$.dirty[0]&131073|n.$$.dirty[1]&1&&JSON.stringify(o)!==JSON.stringify(r)&&(t(31,r=o),g.dispatch("change"))},[o,b,l,a,i,s,h,u,c,m,O,U,d,v,D,N,P,g,W,K,V,Q,C,A,T,J,R,te,ae,ie,M,r,L,se,oe,ue,re,_e,_,Se,je,Ee,De,Ne,Pe,Ue,Je,Le,Oe,We,qe,Ce,Ke,Me]}class kl extends ke{constructor(e){super(),pe(this,e,vl,wl,de,{elem_id:2,elem_classes:3,visible:4,value:0,label:5,sources:6,root:7,show_label:8,loading_status:1,height:9,width:10,container:11,scale:12,min_width:13,autoplay:14,show_share_button:15,show_download_button:16,gradio:17,interactive:18,mirror_webcam:19,include_audio:20,loop:21,input_ready:30},null,[-1,-1])}get elem_id(){return this.$$.ctx[2]}set elem_id(e){this.$$set({elem_id:e}),w()}get elem_classes(){return this.$$.ctx[3]}set elem_classes(e){this.$$set({elem_classes:e}),w()}get visible(){return this.$$.ctx[4]}set visible(e){this.$$set({visible:e}),w()}get value(){return this.$$.ctx[0]}set value(e){this.$$set({value:e}),w()}get label(){return this.$$.ctx[5]}set label(e){this.$$set({label:e}),w()}get sources(){return this.$$.ctx[6]}set sources(e){this.$$set({sources:e}),w()}get root(){return this.$$.ctx[7]}set root(e){this.$$set({root:e}),w()}get show_label(){return this.$$.ctx[8]}set show_label(e){this.$$set({show_label:e}),w()}get loading_status(){return this.$$.ctx[1]}set loading_status(e){this.$$set({loading_status:e}),w()}get height(){return this.$$.ctx[9]}set height(e){this.$$set({height:e}),w()}get width(){return this.$$.ctx[10]}set width(e){this.$$set({width:e}),w()}get container(){return this.$$.ctx[11]}set container(e){this.$$set({container:e}),w()}get scale(){return this.$$.ctx[12]}set scale(e){this.$$set({scale:e}),w()}get min_width(){return this.$$.ctx[13]}set min_width(e){this.$$set({min_width:e}),w()}get autoplay(){return this.$$.ctx[14]}set autoplay(e){this.$$set({autoplay:e}),w()}get show_share_button(){return this.$$.ctx[15]}set show_share_button(e){this.$$set({show_share_button:e}),w()}get show_download_button(){return this.$$.ctx[16]}set show_download_button(e){this.$$set({show_download_button:e}),w()}get gradio(){return this.$$.ctx[17]}set gradio(e){this.$$set({gradio:e}),w()}get interactive(){return this.$$.ctx[18]}set interactive(e){this.$$set({interactive:e}),w()}get mirror_webcam(){return this.$$.ctx[19]}set mirror_webcam(e){this.$$set({mirror_webcam:e}),w()}get include_audio(){return this.$$.ctx[20]}set include_audio(e){this.$$set({include_audio:e}),w()}get loop(){return this.$$.ctx[21]}set loop(e){this.$$set({loop:e}),w()}get input_ready(){return this.$$.ctx[30]}set input_ready(e){this.$$set({input_ready:e}),w()}}const Wl=kl;export{Tl as BaseExample,hl as BaseInteractiveVideo,el as BasePlayer,ll as BaseStaticVideo,Wl as default,Kl as loaded,xe as playable,be as prettyBytes};
