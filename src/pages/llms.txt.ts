import { getCollection } from 'astro:content';
import type { APIRoute } from 'astro';
import { siteConfig } from '../config/site';
import { countTags, postMarkdownUrl, postUrl, sortPosts } from '../utils/posts';

export const GET: APIRoute = async () => {
	const posts = sortPosts(await getCollection('blog'));
	const topics = countTags(posts)
		.slice(0, 12)
		.map(({ tag }) => tag)
		.join(', ');
	const { author } = siteConfig;

	const lines = [
		`# ${siteConfig.title}`,
		'',
		`> OpenDoors (opendoors.wtf) is the technical blog of ${author.name}, a backend engineer in New York. It covers reverse engineering, security research, malware analysis, AI infrastructure security and backend engineering.`,
		'',
		`Author: ${author.name}, also known as ${author.alternateName.slice(0, 2).join(' and ')}. ${author.bio}`,
		`Main topics: ${topics}.`,
		'Every post is also available as plain Markdown at the same URL with .md instead of a trailing slash.',
		'',
		'## Posts',
		'',
		...posts.map(
			(post) =>
				`- [${post.data.title}](${postUrl(post)}): ${post.data.description} (${post.data.pubDate.toISOString().slice(0, 10)}, Markdown: ${postMarkdownUrl(post)})`,
		),
		'',
		'## Author',
		'',
		`- [Portfolio](${author.url}): ${author.name}'s portfolio and work`,
		`- [GitHub](${siteConfig.socials.github}): source code for the tools written about here`,
		`- [X](${siteConfig.socials.x})`,
		`- [LinkedIn](${siteConfig.socials.linkedin})`,
		`- Contact: ${author.email}`,
		'',
		'## Projects',
		'',
		...siteConfig.projects.map((project) => `- [${project.name}](${project.url}): ${project.blurb}`),
		'',
		'## Optional',
		'',
		`- [Full text of every post](${siteConfig.site}/llms-full.txt)`,
		`- [RSS feed](${siteConfig.site}/rss.xml)`,
		`- [Sitemap](${siteConfig.site}/sitemap-index.xml)`,
		'',
	];

	return new Response(lines.join('\n'), {
		headers: { 'Content-Type': 'text/plain; charset=utf-8' },
	});
};
