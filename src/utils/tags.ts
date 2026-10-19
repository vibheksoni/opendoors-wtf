const SPECIAL_WORDS: Record<string, string> = {
	ai: 'AI',
	api: 'API',
	dma: 'DMA',
	rce: 'RCE',
	mcp: 'MCP',
	llm: 'LLM',
	devsecops: 'DevSecOps',
	javascript: 'JavaScript',
	typescript: 'TypeScript',
	lmstudio: 'LM Studio',
	ollama: 'Ollama',
	bun: 'Bun',
};

export function toSlug(tag: string): string {
	return tag.trim().toLowerCase().replace(/\s+/g, '-');
}

export function toTitle(tag: string): string {
	return tag
		.trim()
		.split(/\s+/g)
		.map((word) => SPECIAL_WORDS[word.toLowerCase()] ?? word.charAt(0).toUpperCase() + word.slice(1))
		.join(' ');
}
