import type { CollectionEntry } from 'astro:content';
import { siteConfig } from '../config/site';

export function sortPosts(posts: CollectionEntry<'blog'>[]): CollectionEntry<'blog'>[] {
	return posts
		.filter((post) => !post.data.draft)
		.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

export function collectTags(posts: CollectionEntry<'blog'>[]): string[] {
	const tags = new Set<string>();

	for (const post of posts) {
		for (const tag of post.data.tags) {
			tags.add(tag);
		}
	}

	return Array.from(tags).sort((a, b) => a.localeCompare(b));
}

export function countTags(posts: CollectionEntry<'blog'>[]): Array<{ tag: string; count: number }> {
	const counts = new Map<string, number>();

	for (const post of posts) {
		for (const tag of post.data.tags) {
			counts.set(tag, (counts.get(tag) ?? 0) + 1);
		}
	}

	return Array.from(counts, ([tag, count]) => ({ tag, count })).sort(
		(a, b) => b.count - a.count || a.tag.localeCompare(b.tag),
	);
}

export function postUrl(post: CollectionEntry<'blog'>): string {
	return `${siteConfig.site}/blog/${post.id}/`;
}

export function postMarkdownUrl(post: CollectionEntry<'blog'>): string {
	return `${siteConfig.site}/blog/${post.id}.md`;
}

export function postMarkdown(post: CollectionEntry<'blog'>): string {
	const body = (post.body ?? '')
		.replace(/^import\s.+$/gm, '')
		.replace(/<Image[^>]*\balt="([^"]*)"[^>]*\/>/g, '[Image: $1]')
		.replace(/<YouTube[^>]*\/>/g, '')
		.replace(/\n{3,}/g, '\n\n')
		.trim();

	return body;
}

export function postWordCount(post: CollectionEntry<'blog'>): number {
	const text = postMarkdown(post).replace(/```[\s\S]*?```/g, ' ');
	return text.split(/\s+/).filter(Boolean).length;
}

export function postAsMarkdownDocument(post: CollectionEntry<'blog'>): string {
	const { title, description, pubDate, updatedDate, tags } = post.data;
	const lines = [
		`# ${title}`,
		'',
		`> ${description}`,
		'',
		`- Author: ${siteConfig.author.name} (${siteConfig.author.url})`,
		`- Published: ${pubDate.toISOString().slice(0, 10)}`,
		updatedDate ? `- Updated: ${updatedDate.toISOString().slice(0, 10)}` : null,
		tags.length ? `- Tags: ${tags.join(', ')}` : null,
		`- URL: ${postUrl(post)}`,
		'',
		postMarkdown(post),
		'',
	];

	return lines.filter((line) => line !== null).join('\n');
}
