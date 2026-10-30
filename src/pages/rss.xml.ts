// src/pages/rss.xml.ts
import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import type { APIContext } from "astro";

export async function GET(context: APIContext) {
  const posts = await getCollection("posts");
  return rss({
    title: "gyuho.me",
    description: "전자전기와 컴퓨터, 수학 그 사이 어딘가.",
    site: context.site!,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.date,
      link: `/${post.id}/`,
    })),
  });
}
