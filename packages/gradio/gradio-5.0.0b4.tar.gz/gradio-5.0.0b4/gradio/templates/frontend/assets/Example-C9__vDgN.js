const{SvelteComponent:g,append:c,attr:_,detach:v,element:f,flush:r,init:y,insert:h,noop:d,safe_not_equal:o,set_data:m,text:b,toggle_class:u}=window.__gradio__svelte__internal;function S(s){let e,a,n=JSON.stringify(s[0],null,2)+"",i;return{c(){e=f("div"),a=f("pre"),i=b(n),_(e,"class","svelte-1ayixqk"),u(e,"table",s[1]==="table"),u(e,"gallery",s[1]==="gallery"),u(e,"selected",s[2])},m(l,t){h(l,e,t),c(e,a),c(a,i)},p(l,[t]){t&1&&n!==(n=JSON.stringify(l[0],null,2)+"")&&m(i,n),t&2&&u(e,"table",l[1]==="table"),t&2&&u(e,"gallery",l[1]==="gallery"),t&4&&u(e,"selected",l[2])},i:d,o:d,d(l){l&&v(e)}}}function p(s,e,a){let{value:n}=e,{type:i}=e,{selected:l=!1}=e;return s.$$set=t=>{"value"in t&&a(0,n=t.value),"type"in t&&a(1,i=t.type),"selected"in t&&a(2,l=t.selected)},[n,i,l]}class q extends g{constructor(e){super(),y(this,e,p,S,o,{value:0,type:1,selected:2})}get value(){return this.$$.ctx[0]}set value(e){this.$$set({value:e}),r()}get type(){return this.$$.ctx[1]}set type(e){this.$$set({type:e}),r()}get selected(){return this.$$.ctx[2]}set selected(e){this.$$set({selected:e}),r()}}export{q as default};
//# sourceMappingURL=Example-C9__vDgN.js.map
