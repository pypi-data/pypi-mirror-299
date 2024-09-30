import"./index-rhD_mH1q.js";import{B as I}from"./Button-_U8n4zTd.js";import"./svelte/svelte.js";const{SvelteComponent:N,attr:z,create_component:A,create_slot:F,destroy_component:G,detach:D,element:H,flush:o,get_all_dirty_from_scope:J,get_slot_changes:K,init:L,insert:S,mount_component:M,safe_not_equal:O,space:P,src_url_equal:C,transition_in:E,transition_out:j,update_slot_base:Q}=window.__gradio__svelte__internal,{createEventDispatcher:R}=window.__gradio__svelte__internal;function q(l){let e,i,t;return{c(){e=H("img"),z(e,"class","button-icon svelte-yjn27e"),C(e.src,i=l[6].url)||z(e,"src",i),z(e,"alt",t=`${l[5]} icon`)},m(n,s){S(n,e,s)},p(n,s){s&64&&!C(e.src,i=n[6].url)&&z(e,"src",i),s&32&&t!==(t=`${n[5]} icon`)&&z(e,"alt",t)},d(n){n&&D(e)}}}function T(l){let e,i,t=l[6]&&q(l);const n=l[11].default,s=F(n,l,l[12],null);return{c(){t&&t.c(),e=P(),s&&s.c()},m(_,c){t&&t.m(_,c),S(_,e,c),s&&s.m(_,c),i=!0},p(_,c){_[6]?t?t.p(_,c):(t=q(_),t.c(),t.m(e.parentNode,e)):t&&(t.d(1),t=null),s&&s.p&&(!i||c&4096)&&Q(s,n,_,_[12],i?K(n,_[12],c,null):J(_[12]),null)},i(_){i||(E(s,_),i=!0)},o(_){j(s,_),i=!1},d(_){_&&D(e),t&&t.d(_),s&&s.d(_)}}}function U(l){let e,i;return e=new I({props:{size:l[4],variant:l[3],elem_id:l[0],elem_classes:l[1],visible:l[2],scale:l[8],min_width:l[9],disabled:l[7],$$slots:{default:[T]},$$scope:{ctx:l}}}),e.$on("click",l[10]),{c(){A(e.$$.fragment)},m(t,n){M(e,t,n),i=!0},p(t,[n]){const s={};n&16&&(s.size=t[4]),n&8&&(s.variant=t[3]),n&1&&(s.elem_id=t[0]),n&2&&(s.elem_classes=t[1]),n&4&&(s.visible=t[2]),n&256&&(s.scale=t[8]),n&512&&(s.min_width=t[9]),n&128&&(s.disabled=t[7]),n&4192&&(s.$$scope={dirty:n,ctx:t}),e.$set(s)},i(t){i||(E(e.$$.fragment,t),i=!0)},o(t){j(e.$$.fragment,t),i=!1},d(t){G(e,t)}}}function V(l,e,i){let{$$slots:t={},$$scope:n}=e,{elem_id:s=""}=e,{elem_classes:_=[]}=e,{visible:c=!0}=e,{variant:h="secondary"}=e,{size:d="lg"}=e,{value:m}=e,{icon:g}=e,{disabled:b=!1}=e,{scale:v=null}=e,{min_width:r=void 0}=e;const k=R();function u(){if(k("click"),!m?.url)return;let a;if(!m.orig_name&&m.url){const B=m.url.split("/");a=B[B.length-1],a=a.split("?")[0].split("#")[0]}else a=m.orig_name;const w=document.createElement("a");w.href=m.url,w.download=a||"file",document.body.appendChild(w),w.click(),document.body.removeChild(w)}return l.$$set=a=>{"elem_id"in a&&i(0,s=a.elem_id),"elem_classes"in a&&i(1,_=a.elem_classes),"visible"in a&&i(2,c=a.visible),"variant"in a&&i(3,h=a.variant),"size"in a&&i(4,d=a.size),"value"in a&&i(5,m=a.value),"icon"in a&&i(6,g=a.icon),"disabled"in a&&i(7,b=a.disabled),"scale"in a&&i(8,v=a.scale),"min_width"in a&&i(9,r=a.min_width),"$$scope"in a&&i(12,n=a.$$scope)},[s,_,c,h,d,m,g,b,v,r,u,t,n]}class W extends N{constructor(e){super(),L(this,e,V,U,O,{elem_id:0,elem_classes:1,visible:2,variant:3,size:4,value:5,icon:6,disabled:7,scale:8,min_width:9})}get elem_id(){return this.$$.ctx[0]}set elem_id(e){this.$$set({elem_id:e}),o()}get elem_classes(){return this.$$.ctx[1]}set elem_classes(e){this.$$set({elem_classes:e}),o()}get visible(){return this.$$.ctx[2]}set visible(e){this.$$set({visible:e}),o()}get variant(){return this.$$.ctx[3]}set variant(e){this.$$set({variant:e}),o()}get size(){return this.$$.ctx[4]}set size(e){this.$$set({size:e}),o()}get value(){return this.$$.ctx[5]}set value(e){this.$$set({value:e}),o()}get icon(){return this.$$.ctx[6]}set icon(e){this.$$set({icon:e}),o()}get disabled(){return this.$$.ctx[7]}set disabled(e){this.$$set({disabled:e}),o()}get scale(){return this.$$.ctx[8]}set scale(e){this.$$set({scale:e}),o()}get min_width(){return this.$$.ctx[9]}set min_width(e){this.$$set({min_width:e}),o()}}const X=W,{SvelteComponent:Y,create_component:Z,destroy_component:y,detach:x,flush:f,init:$,insert:p,mount_component:ee,safe_not_equal:te,set_data:ie,text:ne,transition_in:se,transition_out:le}=window.__gradio__svelte__internal;function ae(l){let e=(l[10]?l[11].i18n(l[10]):"")+"",i;return{c(){i=ne(e)},m(t,n){p(t,i,n)},p(t,n){n&3072&&e!==(e=(t[10]?t[11].i18n(t[10]):"")+"")&&ie(i,e)},d(t){t&&x(i)}}}function ue(l){let e,i;return e=new X({props:{value:l[3],variant:l[4],elem_id:l[0],elem_classes:l[1],size:l[6],scale:l[7],icon:l[8],min_width:l[9],visible:l[2],disabled:!l[5],$$slots:{default:[ae]},$$scope:{ctx:l}}}),e.$on("click",l[12]),{c(){Z(e.$$.fragment)},m(t,n){ee(e,t,n),i=!0},p(t,[n]){const s={};n&8&&(s.value=t[3]),n&16&&(s.variant=t[4]),n&1&&(s.elem_id=t[0]),n&2&&(s.elem_classes=t[1]),n&64&&(s.size=t[6]),n&128&&(s.scale=t[7]),n&256&&(s.icon=t[8]),n&512&&(s.min_width=t[9]),n&4&&(s.visible=t[2]),n&32&&(s.disabled=!t[5]),n&11264&&(s.$$scope={dirty:n,ctx:t}),e.$set(s)},i(t){i||(se(e.$$.fragment,t),i=!0)},o(t){le(e.$$.fragment,t),i=!1},d(t){y(e,t)}}}function _e(l,e,i){let{elem_id:t=""}=e,{elem_classes:n=[]}=e,{visible:s=!0}=e,{value:_}=e,{variant:c="secondary"}=e,{interactive:h}=e,{size:d="lg"}=e,{scale:m=null}=e,{icon:g=null}=e,{min_width:b=void 0}=e,{label:v=null}=e,{gradio:r}=e;const k=()=>r.dispatch("click");return l.$$set=u=>{"elem_id"in u&&i(0,t=u.elem_id),"elem_classes"in u&&i(1,n=u.elem_classes),"visible"in u&&i(2,s=u.visible),"value"in u&&i(3,_=u.value),"variant"in u&&i(4,c=u.variant),"interactive"in u&&i(5,h=u.interactive),"size"in u&&i(6,d=u.size),"scale"in u&&i(7,m=u.scale),"icon"in u&&i(8,g=u.icon),"min_width"in u&&i(9,b=u.min_width),"label"in u&&i(10,v=u.label),"gradio"in u&&i(11,r=u.gradio)},[t,n,s,_,c,h,d,m,g,b,v,r,k]}class oe extends Y{constructor(e){super(),$(this,e,_e,ue,te,{elem_id:0,elem_classes:1,visible:2,value:3,variant:4,interactive:5,size:6,scale:7,icon:8,min_width:9,label:10,gradio:11})}get elem_id(){return this.$$.ctx[0]}set elem_id(e){this.$$set({elem_id:e}),f()}get elem_classes(){return this.$$.ctx[1]}set elem_classes(e){this.$$set({elem_classes:e}),f()}get visible(){return this.$$.ctx[2]}set visible(e){this.$$set({visible:e}),f()}get value(){return this.$$.ctx[3]}set value(e){this.$$set({value:e}),f()}get variant(){return this.$$.ctx[4]}set variant(e){this.$$set({variant:e}),f()}get interactive(){return this.$$.ctx[5]}set interactive(e){this.$$set({interactive:e}),f()}get size(){return this.$$.ctx[6]}set size(e){this.$$set({size:e}),f()}get scale(){return this.$$.ctx[7]}set scale(e){this.$$set({scale:e}),f()}get icon(){return this.$$.ctx[8]}set icon(e){this.$$set({icon:e}),f()}get min_width(){return this.$$.ctx[9]}set min_width(e){this.$$set({min_width:e}),f()}get label(){return this.$$.ctx[10]}set label(e){this.$$set({label:e}),f()}get gradio(){return this.$$.ctx[11]}set gradio(e){this.$$set({gradio:e}),f()}}export{X as BaseButton,oe as default};
//# sourceMappingURL=Index-Dhg310jU.js.map
