import { c as create_ssr_component, v as validate_component } from './ssr-Cz1f32Mr.js';
import './2-DpTvHskm.js';
import { I as Image$1 } from './Image2-CIpzhHTx.js';
import './index4-D_FyJKAV.js';
import './file-url-D-K40zdU.js';

/* empty css                                       */
const css = {
  code: ".container.svelte-7kb74g img{width:100%;height:100%}.container.selected.svelte-7kb74g{border-color:var(--border-color-accent)}.container.table.svelte-7kb74g{margin:0 auto;border:2px solid var(--border-color-primary);border-radius:var(--radius-lg);width:var(--size-20);height:var(--size-20);object-fit:cover}.container.gallery.svelte-7kb74g{border:2px solid var(--border-color-primary);height:var(--size-20);max-height:var(--size-20);object-fit:cover}",
  map: '{"version":3,"file":"Example.svelte","sources":["Example.svelte"],"sourcesContent":["<script lang=\\"ts\\">import { BaseImage as Image } from \\"@gradio/image\\";\\nexport let value;\\nexport let type;\\nexport let selected = false;\\n<\/script>\\n\\n<div\\n\\tclass=\\"container\\"\\n\\tclass:table={type === \\"table\\"}\\n\\tclass:gallery={type === \\"gallery\\"}\\n\\tclass:selected\\n>\\n\\t<Image src={value.composite?.url || value.background?.url} alt=\\"\\" />\\n</div>\\n\\n<style>\\n\\t.container :global(img) {\\n\\t\\twidth: 100%;\\n\\t\\theight: 100%;\\n\\t}\\n\\n\\t.container.selected {\\n\\t\\tborder-color: var(--border-color-accent);\\n\\t}\\n\\n\\t.container.table {\\n\\t\\tmargin: 0 auto;\\n\\t\\tborder: 2px solid var(--border-color-primary);\\n\\t\\tborder-radius: var(--radius-lg);\\n\\t\\twidth: var(--size-20);\\n\\t\\theight: var(--size-20);\\n\\t\\tobject-fit: cover;\\n\\t}\\n\\n\\t.container.gallery {\\n\\t\\tborder: 2px solid var(--border-color-primary);\\n\\t\\theight: var(--size-20);\\n\\t\\tmax-height: var(--size-20);\\n\\t\\tobject-fit: cover;\\n\\t}\\n</style>\\n"],"names":[],"mappings":"AAgBC,wBAAU,CAAS,GAAK,CACvB,KAAK,CAAE,IAAI,CACX,MAAM,CAAE,IACT,CAEA,UAAU,uBAAU,CACnB,YAAY,CAAE,IAAI,qBAAqB,CACxC,CAEA,UAAU,oBAAO,CAChB,MAAM,CAAE,CAAC,CAAC,IAAI,CACd,MAAM,CAAE,GAAG,CAAC,KAAK,CAAC,IAAI,sBAAsB,CAAC,CAC7C,aAAa,CAAE,IAAI,WAAW,CAAC,CAC/B,KAAK,CAAE,IAAI,SAAS,CAAC,CACrB,MAAM,CAAE,IAAI,SAAS,CAAC,CACtB,UAAU,CAAE,KACb,CAEA,UAAU,sBAAS,CAClB,MAAM,CAAE,GAAG,CAAC,KAAK,CAAC,IAAI,sBAAsB,CAAC,CAC7C,MAAM,CAAE,IAAI,SAAS,CAAC,CACtB,UAAU,CAAE,IAAI,SAAS,CAAC,CAC1B,UAAU,CAAE,KACb"}'
};
const Example = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { value } = $$props;
  let { type } = $$props;
  let { selected = false } = $$props;
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.type === void 0 && $$bindings.type && type !== void 0)
    $$bindings.type(type);
  if ($$props.selected === void 0 && $$bindings.selected && selected !== void 0)
    $$bindings.selected(selected);
  $$result.css.add(css);
  return `<div class="${[
    "container svelte-7kb74g",
    (type === "table" ? "table" : "") + " " + (type === "gallery" ? "gallery" : "") + " " + (selected ? "selected" : "")
  ].join(" ").trim()}">${validate_component(Image$1, "Image").$$render(
    $$result,
    {
      src: value.composite?.url || value.background?.url,
      alt: ""
    },
    {},
    {}
  )} </div>`;
});

export { Example as default };
//# sourceMappingURL=Example16-BUZJAU5t.js.map
