import{I as u}from"./IconButton-DBg6YGHG.js";import{C as _}from"./Community-CC3ywblm.js";import"./IconButtonWrapper.svelte_svelte_type_style_lang-Cdolb8gF.js";import{S as h}from"./utils-BiWkKWez.js";const{SvelteComponent:g,create_component:d,destroy_component:v,flush:c,init:w,mount_component:S,safe_not_equal:p,transition_in:b,transition_out:y}=window.__gradio__svelte__internal,{createEventDispatcher:C}=window.__gradio__svelte__internal;function I(i){let t,r;return t=new u({props:{Icon:_,label:i[2]("common.share"),pending:i[3]}}),t.$on("click",i[5]),{c(){d(t.$$.fragment)},m(e,o){S(t,e,o),r=!0},p(e,[o]){const a={};o&4&&(a.label=e[2]("common.share")),o&8&&(a.pending=e[3]),t.$set(a)},i(e){r||(b(t.$$.fragment,e),r=!0)},o(e){y(t.$$.fragment,e),r=!1},d(e){v(t,e)}}}function k(i,t,r){const e=C();let{formatter:o}=t,{value:a}=t,{i18n:m}=t,s=!1;const l=async()=>{try{r(3,s=!0);const n=await o(a);e("share",{description:n})}catch(n){console.error(n);let f=n instanceof h?n.message:"Share failed.";e("error",f)}finally{r(3,s=!1)}};return i.$$set=n=>{"formatter"in n&&r(0,o=n.formatter),"value"in n&&r(1,a=n.value),"i18n"in n&&r(2,m=n.i18n)},[o,a,m,s,e,l]}class D extends g{constructor(t){super(),w(this,t,k,I,p,{formatter:0,value:1,i18n:2})}get formatter(){return this.$$.ctx[0]}set formatter(t){this.$$set({formatter:t}),c()}get value(){return this.$$.ctx[1]}set value(t){this.$$set({value:t}),c()}get i18n(){return this.$$.ctx[2]}set i18n(t){this.$$set({i18n:t}),c()}}export{D as S};
//# sourceMappingURL=ShareButton-BAtA0g51.js.map
