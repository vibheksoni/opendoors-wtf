import { getCollection } from 'astro:content';
import rss from '@astrojs/rss';
import { siteConfig } from '../config/site';
import { SITE_DESCRIPTION, SITE_TITLE } from '../consts';
import { sortPosts } from '../utils/posts';

export async function GET(context) {
	const posts = sortPosts(await getCollection('blog'));
	return rss({
		title: SITE_TITLE,
		description: SITE_DESCRIPTION,
		site: context.site,
		trailingSlash: true,
		customData: `<language>en-us</language><copyright>${new Date().getFullYear()} ${siteConfig.author.name}</copyright>`,
		items: posts.map((post) => ({
			title: post.data.title,
			description: post.data.description,
			pubDate: post.data.pubDate,
			link: `/blog/${post.id}/`,
			categories: post.data.tags,
			author: `${siteConfig.author.email} (${siteConfig.author.name})`,
		})),
	});
}
