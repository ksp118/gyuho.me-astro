// @ts-check
import { unified } from "@astrojs/markdown-remark";
import { defineConfig } from "astro/config";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

/** @type {import('@astrojs/markdown-remark').RehypePlugin} */
function rehypeKatexStrict() {
  const isBuild = process.env.NODE_ENV === "production";
  return (tree, file) => {
    const errors = file.messages.filter((m) => m.source === "rehype-katex");
    if (errors.length === 0) return;

    const detail = errors
      .map((m) => `  ${m.line}:${m.column} ${m.cause ?? m.reason}`)
      .join("\n");
    const msg = `KaTeX errors in ${file.path}:\n${detail}`;
    if (!isBuild) {
      console.warn(msg);
      return;
    }
    throw new Error(msg);
  };
}

// https://astro.build/config
export default defineConfig({
  site: "https://gyuho.me",
  trailingSlash: "always",
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex, rehypeKatexStrict],
    }),
    shikiConfig: { theme: "min-light" },
  },
});
