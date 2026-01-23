// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';
import embeds from 'astro-embed/integration';

export default defineConfig({
	site: 'https://opendoors.wtf',
	integrations: [embeds(), mdx(), sitemap()],
	output: 'static',
	devToolbar: {
		enabled: false,
	},
});
