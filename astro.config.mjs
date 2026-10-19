// @ts-check

import { readdirSync, readFileSync } from 'node:fs';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

const SITE = 'https://opendoors.wtf';
const BLOG_DIR = new URL('./src/content/blog/', import.meta.url);

const tagCounts = new Map();

function readPostDates() {
	const dates = new Map();
	for (const file of readdirSync(BLOG_DIR)) {
		if (!/\.mdx?$/.test(file)) continue;
		const text = readFileSync(new URL(file, BLOG_DIR), 'utf8');
		const front = text.match(/^---\r?\n([\s\S]*?)\r?\n---/)?.[1] ?? '';
		if (/^draft:\s*true/m.test(front)) continue;
		const updated = front.match(/^updatedDate:\s*["']?([^"'\r\n]+)/m)?.[1];
		const published = front.match(/^pubDate:\s*["']?([^"'\r\n]+)/m)?.[1];
		const value = updated ?? published;
		const tagBlock = front.match(/^tags:[ \t]*\r?\n((?:[ \t]+-.*\r?\n?)+)/m)?.[1] ?? '';
		for (const raw of tagBlock.split(/\r?\n/)) {
			const tag = raw.replace(/^\s*-\s*/, '').replace(/["']/g, '').trim().toLowerCase().replace(/\s+/g, '-');
			if (tag) tagCounts.set(tag, (tagCounts.get(tag) ?? 0) + 1);
		}
		if (value) dates.set(`${SITE}/blog/${file.replace(/\.mdx?$/, '')}/`, new Date(value));
	}
	return dates;
}

const postDates = readPostDates();
const newest = new Date(Math.max(...Array.from(postDates.values(), (date) => date.valueOf())));

export default defineConfig({
	site: SITE,
	integrations: [
		mdx(),
		sitemap({
			filter(page) {
				const tag = page.match(/\/tags\/([^/]+)\/$/)?.[1];
				return !tag || (tagCounts.get(decodeURIComponent(tag)) ?? 0) > 1;
			},
			serialize(item) {
				const date = postDates.get(item.url);
				if (date) {
					item.lastmod = date.toISOString();
				} else if (item.url === `${SITE}/` || item.url === `${SITE}/blog/`) {
					item.lastmod = newest.toISOString();
				}
				return item;
			},
		}),
	],
	output: 'static',
	devToolbar: {
		enabled: false,
	},
});
