import { getCollection } from 'astro:content';
import type { APIRoute } from 'astro';
import { siteConfig } from '../config/site';
import { postAsMarkdownDocument, sortPosts } from '../utils/posts';

export const GET: APIRoute = async () => {
	const posts = sortPosts(await getCollection('blog'));
	const header = [
		`# ${siteConfig.title}: full text`,
		'',
		`> Every post on ${siteConfig.site} by ${siteConfig.author.name} (${siteConfig.author.url}), newest first, as Markdown.`,
		'',
	].join('\n');

	const body = posts.map((post) => postAsMarkdownDocument(post)).join('\n---\n\n');

	return new Response(`${header}\n${body}`, {
		headers: { 'Content-Type': 'text/plain; charset=utf-8' },
	});
};
