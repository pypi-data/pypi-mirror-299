import{s as y,K as o,r as G,a as p,g as $,i as ee,L as H,f as te,B as se}from"./scheduler.xQsDa6L3.js";import{S as le,i as ie,c as v,a as k,m as B,t as b,b as m,d as T,f as J,g as ne,e as ae}from"./index.lnKugwF0.js";import{B as ue,T as _e,d as oe,b as fe,e as he}from"./2.Bbgn9Xo5.js";import{default as Be}from"./Example.gxRIDJCv.js";function M(l){let e,s;const n=[{autoscroll:l[2].autoscroll},{i18n:l[2].i18n},l[19]];let h={};for(let a=0;a<n.length;a+=1)h=se(h,n[a]);return e=new oe({props:h}),e.$on("clear_status",l[26]),{c(){v(e.$$.fragment)},l(a){k(e.$$.fragment,a)},m(a,u){B(e,a,u),s=!0},p(a,u){const r=u[0]&524292?fe(n,[u[0]&4&&{autoscroll:a[2].autoscroll},u[0]&4&&{i18n:a[2].i18n},u[0]&524288&&he(a[19])]):{};e.$set(r)},i(a){s||(b(e.$$.fragment,a),s=!0)},o(a){m(e.$$.fragment,a),s=!1},d(a){T(e,a)}}}function ce(l){let e,s,n,h,a,u=l[19]&&M(l);function r(i){l[27](i)}function g(i){l[28](i)}let c={label:l[3],info:l[4],show_label:l[10],lines:l[8],type:l[12],rtl:l[20],text_align:l[21],max_lines:l[11]?l[11]:l[8]+1,placeholder:l[9],submit_btn:l[16],stop_btn:l[17],show_copy_button:l[18],autofocus:l[22],container:l[13],autoscroll:l[23],max_length:l[25],disabled:!l[24]};return l[0]!==void 0&&(c.value=l[0]),l[1]!==void 0&&(c.value_is_output=l[1]),s=new _e({props:c}),G.push(()=>J(s,"value",r)),G.push(()=>J(s,"value_is_output",g)),s.$on("change",l[29]),s.$on("input",l[30]),s.$on("submit",l[31]),s.$on("blur",l[32]),s.$on("select",l[33]),s.$on("focus",l[34]),s.$on("stop",l[35]),{c(){u&&u.c(),e=p(),v(s.$$.fragment)},l(i){u&&u.l(i),e=$(i),k(s.$$.fragment,i)},m(i,_){u&&u.m(i,_),ee(i,e,_),B(s,i,_),a=!0},p(i,_){i[19]?u?(u.p(i,_),_[0]&524288&&b(u,1)):(u=M(i),u.c(),b(u,1),u.m(e.parentNode,e)):u&&(ne(),m(u,1,1,()=>{u=null}),ae());const f={};_[0]&8&&(f.label=i[3]),_[0]&16&&(f.info=i[4]),_[0]&1024&&(f.show_label=i[10]),_[0]&256&&(f.lines=i[8]),_[0]&4096&&(f.type=i[12]),_[0]&1048576&&(f.rtl=i[20]),_[0]&2097152&&(f.text_align=i[21]),_[0]&2304&&(f.max_lines=i[11]?i[11]:i[8]+1),_[0]&512&&(f.placeholder=i[9]),_[0]&65536&&(f.submit_btn=i[16]),_[0]&131072&&(f.stop_btn=i[17]),_[0]&262144&&(f.show_copy_button=i[18]),_[0]&4194304&&(f.autofocus=i[22]),_[0]&8192&&(f.container=i[13]),_[0]&8388608&&(f.autoscroll=i[23]),_[0]&33554432&&(f.max_length=i[25]),_[0]&16777216&&(f.disabled=!i[24]),!n&&_[0]&1&&(n=!0,f.value=i[0],H(()=>n=!1)),!h&&_[0]&2&&(h=!0,f.value_is_output=i[1],H(()=>h=!1)),s.$set(f)},i(i){a||(b(u),b(s.$$.fragment,i),a=!0)},o(i){m(u),m(s.$$.fragment,i),a=!1},d(i){i&&te(e),u&&u.d(i),T(s,i)}}}function re(l){let e,s;return e=new ue({props:{visible:l[7],elem_id:l[5],elem_classes:l[6],scale:l[14],min_width:l[15],allow_overflow:!1,padding:l[13],$$slots:{default:[ce]},$$scope:{ctx:l}}}),{c(){v(e.$$.fragment)},l(n){k(e.$$.fragment,n)},m(n,h){B(e,n,h),s=!0},p(n,h){const a={};h[0]&128&&(a.visible=n[7]),h[0]&32&&(a.elem_id=n[5]),h[0]&64&&(a.elem_classes=n[6]),h[0]&16384&&(a.scale=n[14]),h[0]&32768&&(a.min_width=n[15]),h[0]&8192&&(a.padding=n[13]),h[0]&67059487|h[1]&32&&(a.$$scope={dirty:h,ctx:n}),e.$set(a)},i(n){s||(b(e.$$.fragment,n),s=!0)},o(n){m(e.$$.fragment,n),s=!1},d(n){T(e,n)}}}function be(l,e,s){let{gradio:n}=e,{label:h="Textbox"}=e,{info:a=void 0}=e,{elem_id:u=""}=e,{elem_classes:r=[]}=e,{visible:g=!0}=e,{value:c=""}=e,{lines:i}=e,{placeholder:_=""}=e,{show_label:f}=e,{max_lines:x}=e,{type:S="text"}=e,{container:j=!0}=e,{scale:q=null}=e,{min_width:C=void 0}=e,{submit_btn:E=null}=e,{stop_btn:I=null}=e,{show_copy_button:K=!1}=e,{loading_status:w=void 0}=e,{value_is_output:d=!1}=e,{rtl:L=!1}=e,{text_align:N=void 0}=e,{autofocus:z=!1}=e,{autoscroll:A=!0}=e,{interactive:D}=e,{max_length:F=void 0}=e;const O=()=>n.dispatch("clear_status",w);function P(t){c=t,s(0,c)}function Q(t){d=t,s(1,d)}const R=()=>n.dispatch("change",c),U=()=>n.dispatch("input"),V=()=>n.dispatch("submit"),W=()=>n.dispatch("blur"),X=t=>n.dispatch("select",t.detail),Y=()=>n.dispatch("focus"),Z=()=>n.dispatch("stop");return l.$$set=t=>{"gradio"in t&&s(2,n=t.gradio),"label"in t&&s(3,h=t.label),"info"in t&&s(4,a=t.info),"elem_id"in t&&s(5,u=t.elem_id),"elem_classes"in t&&s(6,r=t.elem_classes),"visible"in t&&s(7,g=t.visible),"value"in t&&s(0,c=t.value),"lines"in t&&s(8,i=t.lines),"placeholder"in t&&s(9,_=t.placeholder),"show_label"in t&&s(10,f=t.show_label),"max_lines"in t&&s(11,x=t.max_lines),"type"in t&&s(12,S=t.type),"container"in t&&s(13,j=t.container),"scale"in t&&s(14,q=t.scale),"min_width"in t&&s(15,C=t.min_width),"submit_btn"in t&&s(16,E=t.submit_btn),"stop_btn"in t&&s(17,I=t.stop_btn),"show_copy_button"in t&&s(18,K=t.show_copy_button),"loading_status"in t&&s(19,w=t.loading_status),"value_is_output"in t&&s(1,d=t.value_is_output),"rtl"in t&&s(20,L=t.rtl),"text_align"in t&&s(21,N=t.text_align),"autofocus"in t&&s(22,z=t.autofocus),"autoscroll"in t&&s(23,A=t.autoscroll),"interactive"in t&&s(24,D=t.interactive),"max_length"in t&&s(25,F=t.max_length)},[c,d,n,h,a,u,r,g,i,_,f,x,S,j,q,C,E,I,K,w,L,N,z,A,D,F,O,P,Q,R,U,V,W,X,Y,Z]}class we extends le{constructor(e){super(),ie(this,e,be,re,y,{gradio:2,label:3,info:4,elem_id:5,elem_classes:6,visible:7,value:0,lines:8,placeholder:9,show_label:10,max_lines:11,type:12,container:13,scale:14,min_width:15,submit_btn:16,stop_btn:17,show_copy_button:18,loading_status:19,value_is_output:1,rtl:20,text_align:21,autofocus:22,autoscroll:23,interactive:24,max_length:25},null,[-1,-1])}get gradio(){return this.$$.ctx[2]}set gradio(e){this.$$set({gradio:e}),o()}get label(){return this.$$.ctx[3]}set label(e){this.$$set({label:e}),o()}get info(){return this.$$.ctx[4]}set info(e){this.$$set({info:e}),o()}get elem_id(){return this.$$.ctx[5]}set elem_id(e){this.$$set({elem_id:e}),o()}get elem_classes(){return this.$$.ctx[6]}set elem_classes(e){this.$$set({elem_classes:e}),o()}get visible(){return this.$$.ctx[7]}set visible(e){this.$$set({visible:e}),o()}get value(){return this.$$.ctx[0]}set value(e){this.$$set({value:e}),o()}get lines(){return this.$$.ctx[8]}set lines(e){this.$$set({lines:e}),o()}get placeholder(){return this.$$.ctx[9]}set placeholder(e){this.$$set({placeholder:e}),o()}get show_label(){return this.$$.ctx[10]}set show_label(e){this.$$set({show_label:e}),o()}get max_lines(){return this.$$.ctx[11]}set max_lines(e){this.$$set({max_lines:e}),o()}get type(){return this.$$.ctx[12]}set type(e){this.$$set({type:e}),o()}get container(){return this.$$.ctx[13]}set container(e){this.$$set({container:e}),o()}get scale(){return this.$$.ctx[14]}set scale(e){this.$$set({scale:e}),o()}get min_width(){return this.$$.ctx[15]}set min_width(e){this.$$set({min_width:e}),o()}get submit_btn(){return this.$$.ctx[16]}set submit_btn(e){this.$$set({submit_btn:e}),o()}get stop_btn(){return this.$$.ctx[17]}set stop_btn(e){this.$$set({stop_btn:e}),o()}get show_copy_button(){return this.$$.ctx[18]}set show_copy_button(e){this.$$set({show_copy_button:e}),o()}get loading_status(){return this.$$.ctx[19]}set loading_status(e){this.$$set({loading_status:e}),o()}get value_is_output(){return this.$$.ctx[1]}set value_is_output(e){this.$$set({value_is_output:e}),o()}get rtl(){return this.$$.ctx[20]}set rtl(e){this.$$set({rtl:e}),o()}get text_align(){return this.$$.ctx[21]}set text_align(e){this.$$set({text_align:e}),o()}get autofocus(){return this.$$.ctx[22]}set autofocus(e){this.$$set({autofocus:e}),o()}get autoscroll(){return this.$$.ctx[23]}set autoscroll(e){this.$$set({autoscroll:e}),o()}get interactive(){return this.$$.ctx[24]}set interactive(e){this.$$set({interactive:e}),o()}get max_length(){return this.$$.ctx[25]}set max_length(e){this.$$set({max_length:e}),o()}}export{Be as BaseExample,_e as BaseTextbox,we as default};
