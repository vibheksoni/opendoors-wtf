import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
	loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			draft: z.boolean().default(false),
			canonical: z.string().url().optional(),
			tags: z.array(z.string()).default([]),
			heroImage: image().optional(),
			youtube: z.string().url().optional(),
		}),
});

export const collections = { blog };
