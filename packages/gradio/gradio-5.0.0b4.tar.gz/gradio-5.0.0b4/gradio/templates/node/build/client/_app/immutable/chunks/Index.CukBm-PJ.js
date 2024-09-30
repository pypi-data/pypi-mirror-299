import{s as ie,e as L,t as G,a as j,c as N,b as I,d as K,f as v,g as T,p as d,q as P,E as H,i as O,h as g,j as p,n as $,y as ue,z as W,Q as _e,F as de,B as me}from"./scheduler.xQsDa6L3.js";import{S as re,i as ce,c as V,a as C,m as J,t as q,b as D,d as z,g as x,e as ee}from"./index.lnKugwF0.js";import{f as le,B as be,d as he,b as ge,e as ve}from"./2.Bbgn9Xo5.js";import{L as oe}from"./LineChart.CQp-JLz8.js";import{B as ke}from"./BlockLabel.EPnqKJ7A.js";import{E as we}from"./Empty.cyjo30Lv.js";function ae(n,l,t){const e=n.slice();return e[5]=l[t],e[7]=t,e}function te(n){let l,t=le(n[0].confidences),e=[];for(let a=0;a<t.length;a+=1)e[a]=ne(ae(n,t,a));return{c(){for(let a=0;a<e.length;a+=1)e[a].c();l=W()},l(a){for(let s=0;s<e.length;s+=1)e[s].l(a);l=W()},m(a,s){for(let i=0;i<e.length;i+=1)e[i]&&e[i].m(a,s);O(a,l,s)},p(a,s){if(s&13){t=le(a[0].confidences);let i;for(i=0;i<t.length;i+=1){const f=ae(a,t,i);e[i]?e[i].p(f,s):(e[i]=ne(f),e[i].c(),e[i].m(l.parentNode,l))}for(;i<e.length;i+=1)e[i].d(1);e.length=t.length}},d(a){a&&v(l),_e(e,a)}}}function ne(n){let l,t,e,a,s,i,f,u,m,c,E=n[5].label+"",b,B,r,_,k,w=Math.round(n[5].confidence*100)+"",S,F,o,Q,X,y;function fe(){return n[4](n[7],n[5])}return{c(){l=L("button"),t=L("div"),e=L("meter"),u=j(),m=L("dl"),c=L("dt"),b=G(E),B=j(),_=L("div"),k=L("dd"),S=G(w),F=G("%"),o=j(),this.h()},l(M){l=N(M,"BUTTON",{class:!0,"data-testid":!0});var h=I(l);t=N(h,"DIV",{class:!0});var R=I(t);e=N(R,"METER",{"aria-labelledby":!0,"aria-label":!0,"aria-valuenow":!0,"aria-valuemin":!0,"aria-valuemax":!0,class:!0,min:!0,max:!0,style:!0}),I(e).forEach(v),u=T(R),m=N(R,"DL",{class:!0});var U=I(m);c=N(U,"DT",{id:!0,class:!0});var Y=I(c);b=K(Y,E),B=T(Y),Y.forEach(v),_=N(U,"DIV",{class:!0}),I(_).forEach(v),k=N(U,"DD",{class:!0});var Z=I(k);S=K(Z,w),F=K(Z,"%"),Z.forEach(v),U.forEach(v),R.forEach(v),o=T(h),h.forEach(v),this.h()},h(){d(e,"aria-labelledby",a=A(`meter-text-${n[5].label}`)),d(e,"aria-label",s=n[5].label),d(e,"aria-valuenow",i=Math.round(n[5].confidence*100)),d(e,"aria-valuemin","0"),d(e,"aria-valuemax","100"),d(e,"class","bar svelte-1iqed6w"),d(e,"min","0"),d(e,"max","1"),e.value=f=n[5].confidence,H(e,"width",n[5].confidence*100+"%"),H(e,"background","var(--stat-background-fill)"),d(c,"id",r=A(`meter-text-${n[5].label}`)),d(c,"class","text svelte-1iqed6w"),d(_,"class","line svelte-1iqed6w"),d(k,"class","confidence svelte-1iqed6w"),d(m,"class","label svelte-1iqed6w"),d(t,"class","inner-wrap svelte-1iqed6w"),d(l,"class","confidence-set group svelte-1iqed6w"),d(l,"data-testid",Q=`${n[5].label}-confidence-set`),P(l,"selectable",n[2])},m(M,h){O(M,l,h),g(l,t),g(t,e),g(t,u),g(t,m),g(m,c),g(c,b),g(c,B),g(m,_),g(m,k),g(k,S),g(k,F),g(l,o),X||(y=de(l,"click",fe),X=!0)},p(M,h){n=M,h&1&&a!==(a=A(`meter-text-${n[5].label}`))&&d(e,"aria-labelledby",a),h&1&&s!==(s=n[5].label)&&d(e,"aria-label",s),h&1&&i!==(i=Math.round(n[5].confidence*100))&&d(e,"aria-valuenow",i),h&1&&f!==(f=n[5].confidence)&&(e.value=f),h&1&&H(e,"width",n[5].confidence*100+"%"),h&1&&E!==(E=n[5].label+"")&&p(b,E),h&1&&r!==(r=A(`meter-text-${n[5].label}`))&&d(c,"id",r),h&1&&w!==(w=Math.round(n[5].confidence*100)+"")&&p(S,w),h&1&&Q!==(Q=`${n[5].label}-confidence-set`)&&d(l,"data-testid",Q),h&4&&P(l,"selectable",n[2])},d(M){M&&v(l),X=!1,y()}}}function Ee(n){let l,t,e=n[0].label+"",a,s,i=typeof n[0]=="object"&&n[0].confidences&&te(n);return{c(){l=L("div"),t=L("h2"),a=G(e),s=j(),i&&i.c(),this.h()},l(f){l=N(f,"DIV",{class:!0});var u=I(l);t=N(u,"H2",{class:!0,"data-testid":!0});var m=I(t);a=K(m,e),m.forEach(v),s=T(u),i&&i.l(u),u.forEach(v),this.h()},h(){d(t,"class","output-class svelte-1iqed6w"),d(t,"data-testid","label-output-value"),P(t,"no-confidence",!("confidences"in n[0])),H(t,"background-color",n[1]||"transparent"),d(l,"class","container svelte-1iqed6w")},m(f,u){O(f,l,u),g(l,t),g(t,a),g(l,s),i&&i.m(l,null)},p(f,[u]){u&1&&e!==(e=f[0].label+"")&&p(a,e),u&1&&P(t,"no-confidence",!("confidences"in f[0])),u&2&&H(t,"background-color",f[1]||"transparent"),typeof f[0]=="object"&&f[0].confidences?i?i.p(f,u):(i=te(f),i.c(),i.m(l,null)):i&&(i.d(1),i=null)},i:$,o:$,d(f){f&&v(l),i&&i.d()}}}function A(n){return n.replace(/\s/g,"-")}function qe(n,l,t){let{value:e}=l;const a=ue();let{color:s=void 0}=l,{selectable:i=!1}=l;const f=(u,m)=>{a("select",{index:u,value:m.label})};return n.$$set=u=>{"value"in u&&t(0,e=u.value),"color"in u&&t(1,s=u.color),"selectable"in u&&t(2,i=u.selectable)},[e,s,i,a,f]}class De extends re{constructor(l){super(),ce(this,l,qe,Ee,ie,{value:0,color:1,selectable:2})}}const Be=De;function se(n){let l,t;return l=new ke({props:{Icon:oe,label:n[6],disable:n[7]===!1}}),{c(){V(l.$$.fragment)},l(e){C(l.$$.fragment,e)},m(e,a){J(l,e,a),t=!0},p(e,a){const s={};a&64&&(s.label=e[6]),a&128&&(s.disable=e[7]===!1),l.$set(s)},i(e){t||(q(l.$$.fragment,e),t=!0)},o(e){D(l.$$.fragment,e),t=!1},d(e){z(l,e)}}}function Le(n){let l,t;return l=new we({props:{unpadded_box:!0,$$slots:{default:[Ie]},$$scope:{ctx:n}}}),{c(){V(l.$$.fragment)},l(e){C(l.$$.fragment,e)},m(e,a){J(l,e,a),t=!0},p(e,a){const s={};a&131072&&(s.$$scope={dirty:a,ctx:e}),l.$set(s)},i(e){t||(q(l.$$.fragment,e),t=!0)},o(e){D(l.$$.fragment,e),t=!1},d(e){z(l,e)}}}function Ne(n){let l,t;return l=new Be({props:{selectable:n[12],value:n[5],color:n[4]}}),l.$on("select",n[16]),{c(){V(l.$$.fragment)},l(e){C(l.$$.fragment,e)},m(e,a){J(l,e,a),t=!0},p(e,a){const s={};a&4096&&(s.selectable=e[12]),a&32&&(s.value=e[5]),a&16&&(s.color=e[4]),l.$set(s)},i(e){t||(q(l.$$.fragment,e),t=!0)},o(e){D(l.$$.fragment,e),t=!1},d(e){z(l,e)}}}function Ie(n){let l,t;return l=new oe({}),{c(){V(l.$$.fragment)},l(e){C(l.$$.fragment,e)},m(e,a){J(l,e,a),t=!0},i(e){t||(q(l.$$.fragment,e),t=!0)},o(e){D(l.$$.fragment,e),t=!1},d(e){z(l,e)}}}function Me(n){let l,t,e,a,s,i,f;const u=[{autoscroll:n[0].autoscroll},{i18n:n[0].i18n},n[10]];let m={};for(let r=0;r<u.length;r+=1)m=me(m,u[r]);l=new he({props:m}),l.$on("clear_status",n[15]);let c=n[11]&&se(n);const E=[Ne,Le],b=[];function B(r,_){return r[13]!==void 0&&r[13]!==null?0:1}return a=B(n),s=b[a]=E[a](n),{c(){V(l.$$.fragment),t=j(),c&&c.c(),e=j(),s.c(),i=W()},l(r){C(l.$$.fragment,r),t=T(r),c&&c.l(r),e=T(r),s.l(r),i=W()},m(r,_){J(l,r,_),O(r,t,_),c&&c.m(r,_),O(r,e,_),b[a].m(r,_),O(r,i,_),f=!0},p(r,_){const k=_&1025?ge(u,[_&1&&{autoscroll:r[0].autoscroll},_&1&&{i18n:r[0].i18n},_&1024&&ve(r[10])]):{};l.$set(k),r[11]?c?(c.p(r,_),_&2048&&q(c,1)):(c=se(r),c.c(),q(c,1),c.m(e.parentNode,e)):c&&(x(),D(c,1,1,()=>{c=null}),ee());let w=a;a=B(r),a===w?b[a].p(r,_):(x(),D(b[w],1,1,()=>{b[w]=null}),ee(),s=b[a],s?s.p(r,_):(s=b[a]=E[a](r),s.c()),q(s,1),s.m(i.parentNode,i))},i(r){f||(q(l.$$.fragment,r),q(c),q(s),f=!0)},o(r){D(l.$$.fragment,r),D(c),D(s),f=!1},d(r){r&&(v(t),v(e),v(i)),z(l,r),c&&c.d(r),b[a].d(r)}}}function Se(n){let l,t;return l=new be({props:{test_id:"label",visible:n[3],elem_id:n[1],elem_classes:n[2],container:n[7],scale:n[8],min_width:n[9],padding:!1,$$slots:{default:[Me]},$$scope:{ctx:n}}}),{c(){V(l.$$.fragment)},l(e){C(l.$$.fragment,e)},m(e,a){J(l,e,a),t=!0},p(e,[a]){const s={};a&8&&(s.visible=e[3]),a&2&&(s.elem_id=e[1]),a&4&&(s.elem_classes=e[2]),a&128&&(s.container=e[7]),a&256&&(s.scale=e[8]),a&512&&(s.min_width=e[9]),a&146673&&(s.$$scope={dirty:a,ctx:e}),l.$set(s)},i(e){t||(q(l.$$.fragment,e),t=!0)},o(e){D(l.$$.fragment,e),t=!1},d(e){z(l,e)}}}function je(n,l,t){let e,{gradio:a}=l,{elem_id:s=""}=l,{elem_classes:i=[]}=l,{visible:f=!0}=l,{color:u=void 0}=l,{value:m={}}=l,c=null,{label:E=a.i18n("label.label")}=l,{container:b=!0}=l,{scale:B=null}=l,{min_width:r=void 0}=l,{loading_status:_}=l,{show_label:k=!0}=l,{_selectable:w=!1}=l;const S=()=>a.dispatch("clear_status",_),F=({detail:o})=>a.dispatch("select",o);return n.$$set=o=>{"gradio"in o&&t(0,a=o.gradio),"elem_id"in o&&t(1,s=o.elem_id),"elem_classes"in o&&t(2,i=o.elem_classes),"visible"in o&&t(3,f=o.visible),"color"in o&&t(4,u=o.color),"value"in o&&t(5,m=o.value),"label"in o&&t(6,E=o.label),"container"in o&&t(7,b=o.container),"scale"in o&&t(8,B=o.scale),"min_width"in o&&t(9,r=o.min_width),"loading_status"in o&&t(10,_=o.loading_status),"show_label"in o&&t(11,k=o.show_label),"_selectable"in o&&t(12,w=o._selectable)},n.$$.update=()=>{n.$$.dirty&16417&&JSON.stringify(m)!==JSON.stringify(c)&&(t(14,c=m),a.dispatch("change")),n.$$.dirty&32&&t(13,e=m.label)},[a,s,i,f,u,m,E,b,B,r,_,k,w,e,c,S,F]}class Fe extends re{constructor(l){super(),ce(this,l,je,Se,ie,{gradio:0,elem_id:1,elem_classes:2,visible:3,color:4,value:5,label:6,container:7,scale:8,min_width:9,loading_status:10,show_label:11,_selectable:12})}}export{Be as BaseLabel,Fe as default};
