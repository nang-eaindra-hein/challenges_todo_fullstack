import tailwindcss from '@tailwindcss/vite';
import adapter from '@sveltejs/adapter-auto';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import Icons from 'unplugin-icons/vite';


export default defineConfig({
	plugins: [
		tailwindcss(),
		Icons({ compiler: 'svelte' }),
		sveltekit({
			compilerOptions: {
				// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
				runes: ({ filename }) =>
					filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			},

			// adapter-auto only supports some environments, see https://svelte.dev/docs/kit/adapter-auto for a list.
			// If your environment is not supported, or you settled on a specific environment, switch out the adapter.
			// See https://svelte.dev/docs/kit/adapters for more information about adapters.
			adapter: adapter()
		})
	],

	// NEW: forward these backend paths to Litestar
	server: {
		proxy: {
			// matches by prefix: /todos, /todo, /todo-status/1, /todo-title/1
			'/todo': 'http://localhost:8000',
			'/delete-todos': 'http://localhost:8000',
			// starts with ^ so Vite reads it as a pattern: matches /5, /12... (delete one)
			'^/\\d+$': 'http://localhost:8000'
		}
	}
});
