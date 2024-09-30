import { c as create_ssr_component, v as validate_component } from './ssr-Cz1f32Mr.js';
import './2-DpTvHskm.js';
import { U as Upload, I as ImagePaste } from './Upload2-CQQNjaMs.js';

const Microphone = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-mic"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>`;
});
const Webcam = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2c-4.963 0-9 4.038-9 9c0 3.328 1.82 6.232 4.513 7.79l-2.067 1.378A1 1 0 0 0 6 22h12a1 1 0 0 0 .555-1.832l-2.067-1.378C19.18 17.232 21 14.328 21 11c0-4.962-4.037-9-9-9zm0 16c-3.859 0-7-3.141-7-7c0-3.86 3.141-7 7-7s7 3.14 7 7c0 3.859-3.141 7-7 7z"></path><path fill="currentColor" d="M12 6c-2.757 0-5 2.243-5 5s2.243 5 5 5s5-2.243 5-5s-2.243-5-5-5zm0 8c-1.654 0-3-1.346-3-3s1.346-3 3-3s3 1.346 3 3s-1.346 3-3 3z"></path></svg>`;
});
const css = {
  code: ".source-selection.svelte-15ls1gu{display:flex;align-items:center;justify-content:center;border-top:1px solid var(--border-color-primary);width:100%;margin-left:auto;margin-right:auto;height:var(--size-10)}.icon.svelte-15ls1gu{width:22px;height:22px;margin:var(--spacing-lg) var(--spacing-xs);padding:var(--spacing-xs);color:var(--neutral-400);border-radius:var(--radius-md)}.selected.svelte-15ls1gu{color:var(--color-accent)}.icon.svelte-15ls1gu:hover,.icon.svelte-15ls1gu:focus{color:var(--color-accent)}",
  map: '{"version":3,"file":"SelectSource.svelte","sources":["SelectSource.svelte"],"sourcesContent":["<script lang=\\"ts\\">import { Microphone, Upload, Webcam, ImagePaste } from \\"@gradio/icons\\";\\nexport let sources;\\nexport let active_source;\\nexport let handle_clear = () => {\\n};\\nexport let handle_select = () => {\\n};\\n$:\\n  unique_sources = [...new Set(sources)];\\nasync function handle_select_source(source) {\\n  handle_clear();\\n  active_source = source;\\n  handle_select(source);\\n}\\n<\/script>\\n\\n{#if unique_sources.length > 1}\\n\\t<span class=\\"source-selection\\" data-testid=\\"source-select\\">\\n\\t\\t{#if sources.includes(\\"upload\\")}\\n\\t\\t\\t<button\\n\\t\\t\\t\\tclass=\\"icon\\"\\n\\t\\t\\t\\tclass:selected={active_source === \\"upload\\" || !active_source}\\n\\t\\t\\t\\taria-label=\\"Upload file\\"\\n\\t\\t\\t\\ton:click={() => handle_select_source(\\"upload\\")}><Upload /></button\\n\\t\\t\\t>\\n\\t\\t{/if}\\n\\n\\t\\t{#if sources.includes(\\"microphone\\")}\\n\\t\\t\\t<button\\n\\t\\t\\t\\tclass=\\"icon\\"\\n\\t\\t\\t\\tclass:selected={active_source === \\"microphone\\"}\\n\\t\\t\\t\\taria-label=\\"Record audio\\"\\n\\t\\t\\t\\ton:click={() => handle_select_source(\\"microphone\\")}\\n\\t\\t\\t\\t><Microphone /></button\\n\\t\\t\\t>\\n\\t\\t{/if}\\n\\n\\t\\t{#if sources.includes(\\"webcam\\")}\\n\\t\\t\\t<button\\n\\t\\t\\t\\tclass=\\"icon\\"\\n\\t\\t\\t\\tclass:selected={active_source === \\"webcam\\"}\\n\\t\\t\\t\\taria-label=\\"Capture from camera\\"\\n\\t\\t\\t\\ton:click={() => handle_select_source(\\"webcam\\")}><Webcam /></button\\n\\t\\t\\t>\\n\\t\\t{/if}\\n\\t\\t{#if sources.includes(\\"clipboard\\")}\\n\\t\\t\\t<button\\n\\t\\t\\t\\tclass=\\"icon\\"\\n\\t\\t\\t\\tclass:selected={active_source === \\"clipboard\\"}\\n\\t\\t\\t\\taria-label=\\"Paste from clipboard\\"\\n\\t\\t\\t\\ton:click={() => handle_select_source(\\"clipboard\\")}\\n\\t\\t\\t\\t><ImagePaste /></button\\n\\t\\t\\t>\\n\\t\\t{/if}\\n\\t</span>\\n{/if}\\n\\n<style>\\n\\t.source-selection {\\n\\t\\tdisplay: flex;\\n\\t\\talign-items: center;\\n\\t\\tjustify-content: center;\\n\\t\\tborder-top: 1px solid var(--border-color-primary);\\n\\t\\twidth: 100%;\\n\\t\\tmargin-left: auto;\\n\\t\\tmargin-right: auto;\\n\\t\\theight: var(--size-10);\\n\\t}\\n\\n\\t.icon {\\n\\t\\twidth: 22px;\\n\\t\\theight: 22px;\\n\\t\\tmargin: var(--spacing-lg) var(--spacing-xs);\\n\\t\\tpadding: var(--spacing-xs);\\n\\t\\tcolor: var(--neutral-400);\\n\\t\\tborder-radius: var(--radius-md);\\n\\t}\\n\\n\\t.selected {\\n\\t\\tcolor: var(--color-accent);\\n\\t}\\n\\n\\t.icon:hover,\\n\\t.icon:focus {\\n\\t\\tcolor: var(--color-accent);\\n\\t}\\n</style>\\n"],"names":[],"mappings":"AA0DC,gCAAkB,CACjB,OAAO,CAAE,IAAI,CACb,WAAW,CAAE,MAAM,CACnB,eAAe,CAAE,MAAM,CACvB,UAAU,CAAE,GAAG,CAAC,KAAK,CAAC,IAAI,sBAAsB,CAAC,CACjD,KAAK,CAAE,IAAI,CACX,WAAW,CAAE,IAAI,CACjB,YAAY,CAAE,IAAI,CAClB,MAAM,CAAE,IAAI,SAAS,CACtB,CAEA,oBAAM,CACL,KAAK,CAAE,IAAI,CACX,MAAM,CAAE,IAAI,CACZ,MAAM,CAAE,IAAI,YAAY,CAAC,CAAC,IAAI,YAAY,CAAC,CAC3C,OAAO,CAAE,IAAI,YAAY,CAAC,CAC1B,KAAK,CAAE,IAAI,aAAa,CAAC,CACzB,aAAa,CAAE,IAAI,WAAW,CAC/B,CAEA,wBAAU,CACT,KAAK,CAAE,IAAI,cAAc,CAC1B,CAEA,oBAAK,MAAM,CACX,oBAAK,MAAO,CACX,KAAK,CAAE,IAAI,cAAc,CAC1B"}'
};
const SelectSource = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let unique_sources;
  let { sources } = $$props;
  let { active_source } = $$props;
  let { handle_clear = () => {
  } } = $$props;
  let { handle_select = () => {
  } } = $$props;
  if ($$props.sources === void 0 && $$bindings.sources && sources !== void 0)
    $$bindings.sources(sources);
  if ($$props.active_source === void 0 && $$bindings.active_source && active_source !== void 0)
    $$bindings.active_source(active_source);
  if ($$props.handle_clear === void 0 && $$bindings.handle_clear && handle_clear !== void 0)
    $$bindings.handle_clear(handle_clear);
  if ($$props.handle_select === void 0 && $$bindings.handle_select && handle_select !== void 0)
    $$bindings.handle_select(handle_select);
  $$result.css.add(css);
  unique_sources = [...new Set(sources)];
  return `${unique_sources.length > 1 ? `<span class="source-selection svelte-15ls1gu" data-testid="source-select">${sources.includes("upload") ? `<button class="${[
    "icon svelte-15ls1gu",
    active_source === "upload" || !active_source ? "selected" : ""
  ].join(" ").trim()}" aria-label="Upload file">${validate_component(Upload, "Upload").$$render($$result, {}, {}, {})}</button>` : ``} ${sources.includes("microphone") ? `<button class="${["icon svelte-15ls1gu", active_source === "microphone" ? "selected" : ""].join(" ").trim()}" aria-label="Record audio">${validate_component(Microphone, "Microphone").$$render($$result, {}, {}, {})}</button>` : ``} ${sources.includes("webcam") ? `<button class="${["icon svelte-15ls1gu", active_source === "webcam" ? "selected" : ""].join(" ").trim()}" aria-label="Capture from camera">${validate_component(Webcam, "Webcam").$$render($$result, {}, {}, {})}</button>` : ``} ${sources.includes("clipboard") ? `<button class="${["icon svelte-15ls1gu", active_source === "clipboard" ? "selected" : ""].join(" ").trim()}" aria-label="Paste from clipboard">${validate_component(ImagePaste, "ImagePaste").$$render($$result, {}, {}, {})}</button>` : ``}</span>` : ``}`;
});

export { SelectSource as S, Webcam as W };
//# sourceMappingURL=SelectSource-CqJII2hd.js.map
