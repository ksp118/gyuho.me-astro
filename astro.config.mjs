// @ts-check
import { unified } from "@astrojs/markdown-remark";
import { defineConfig, fontProviders } from "astro/config";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

import sitemap from "@astrojs/sitemap";

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

  fonts: [
    {
      provider: fontProviders.local(),
      name: "Gyuho Sans",
      cssVariable: "--font-body",
      fallbacks: [],
      options: {
        variants: [
          {
            src: ["./src/assets/fonts/body-400.core.woff2"],
            weight: 400,
            style: "normal",
          },
          {
            src: ["./src/assets/fonts/body-700.core.woff2"],
            weight: 700,
            style: "normal",
          },
        ],
      },
    },
    {
      provider: fontProviders.local(),
      name: "Gyuho Sans Rest",
      cssVariable: "--font-body-rest",
      fallbacks: [],
      options: {
        variants: [
          {
            src: ["./src/assets/fonts/body-400.rest.woff2"],
            weight: 400,
            style: "normal",
            unicodeRange: ["U+AC00-D7A3"],
          },
          {
            src: ["./src/assets/fonts/body-700.rest.woff2"],
            weight: 700,
            style: "normal",
            unicodeRange: ["U+AC00-D7A3"],
          },
        ],
      },
    },
    {
      provider: fontProviders.local(),
      name: "SUIT",
      cssVariable: "--font-head",
      fallbacks: ["sans-serif"],
      options: {
        variants: [
          {
            src: ["./src/assets/fonts/head-700.woff2"],
            weight: 700,
            style: "normal",
          },
        ],
      },
    },
    {
      provider: fontProviders.local(),
      name: "IBM Plex Mono",
      cssVariable: "--font-code",
      fallbacks: [],
      options: {
        variants: [
          {
            src: ["./src/assets/fonts/code-400.woff2"],
            weight: 400,
            style: "normal",
          },
        ],
      },
    },
  ],

  integrations: [sitemap()]
});