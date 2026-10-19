import { getCollection, type CollectionEntry } from 'astro:content';
import type { APIRoute } from 'astro';
import { postAsMarkdownDocument, sortPosts } from '../../utils/posts';

export async function getStaticPaths() {
	const posts = sortPosts(await getCollection('blog'));
	return posts.map((post) => ({
		params: { slug: post.id },
		props: { post },
	}));
}

export const GET: APIRoute = ({ props }) => {
	const { post } = props as { post: CollectionEntry<'blog'> };
	return new Response(postAsMarkdownDocument(post), {
		headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
	});
};
