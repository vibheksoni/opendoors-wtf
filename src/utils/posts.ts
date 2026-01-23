import type { CollectionEntry } from 'astro:content';

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
