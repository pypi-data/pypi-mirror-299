import { c as create_ssr_component, v as validate_component } from './ssr-Cz1f32Mr.js';
import { M as MarkdownCode$1 } from './Example.svelte_svelte_type_style_lang4-BJGUZ_-W.js';
import './prism-python-B-_Fu8f-.js';
import './2-DpTvHskm.js';
import './index4-D_FyJKAV.js';
import './_commonjsHelpers-BFTU3MAI.js';
import 'tty';
import 'path';
import 'url';
import 'fs';

const css = {
  code: ".gallery.svelte-1gecy8w{padding:var(--size-1) var(--size-2)}",
  map: '{"version":3,"file":"Example.svelte","sources":["Example.svelte"],"sourcesContent":["<script lang=\\"ts\\">import MarkdownCode from \\"./shared/MarkdownCode.svelte\\";\\nexport let value;\\nexport let type;\\nexport let selected = false;\\nexport let sanitize_html;\\nexport let line_breaks;\\nexport let latex_delimiters;\\nexport let root;\\n<\/script>\\n\\n<div\\n\\tclass:table={type === \\"table\\"}\\n\\tclass:gallery={type === \\"gallery\\"}\\n\\tclass:selected\\n\\tclass=\\"prose\\"\\n>\\n\\t<MarkdownCode\\n\\t\\tmessage={value ? value : \\"\\"}\\n\\t\\t{latex_delimiters}\\n\\t\\t{sanitize_html}\\n\\t\\t{line_breaks}\\n\\t\\tchatbot={false}\\n\\t\\t{root}\\n\\t/>\\n</div>\\n\\n<style>\\n\\t.gallery {\\n\\t\\tpadding: var(--size-1) var(--size-2);\\n\\t}\\n</style>\\n"],"names":[],"mappings":"AA2BC,uBAAS,CACR,OAAO,CAAE,IAAI,QAAQ,CAAC,CAAC,IAAI,QAAQ,CACpC"}'
};
const Example = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { value } = $$props;
  let { type } = $$props;
  let { selected = false } = $$props;
  let { sanitize_html } = $$props;
  let { line_breaks } = $$props;
  let { latex_delimiters } = $$props;
  let { root } = $$props;
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.type === void 0 && $$bindings.type && type !== void 0)
    $$bindings.type(type);
  if ($$props.selected === void 0 && $$bindings.selected && selected !== void 0)
    $$bindings.selected(selected);
  if ($$props.sanitize_html === void 0 && $$bindings.sanitize_html && sanitize_html !== void 0)
    $$bindings.sanitize_html(sanitize_html);
  if ($$props.line_breaks === void 0 && $$bindings.line_breaks && line_breaks !== void 0)
    $$bindings.line_breaks(line_breaks);
  if ($$props.latex_delimiters === void 0 && $$bindings.latex_delimiters && latex_delimiters !== void 0)
    $$bindings.latex_delimiters(latex_delimiters);
  if ($$props.root === void 0 && $$bindings.root && root !== void 0)
    $$bindings.root(root);
  $$result.css.add(css);
  return `<div class="${[
    "prose svelte-1gecy8w",
    (type === "table" ? "table" : "") + " " + (type === "gallery" ? "gallery" : "") + " " + (selected ? "selected" : "")
  ].join(" ").trim()}">${validate_component(MarkdownCode$1, "MarkdownCode").$$render(
    $$result,
    {
      message: value ? value : "",
      latex_delimiters,
      sanitize_html,
      line_breaks,
      chatbot: false,
      root
    },
    {},
    {}
  )} </div>`;
});

export { Example as default };
//# sourceMappingURL=Example5-DTnQETx-.js.map
