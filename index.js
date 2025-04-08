const fs = require('fs'); // Módulo para manejar el sistema de archivos.
const Parser = require('rss-parser'); // Biblioteca para analizar feeds RSS.
const parser = new Parser();

const ICONS_SIZE_PLACEHOLDER = '%{{icon_size}}%'; // Placeholder para tamaño de íconos.
const ICON_SIZE = '24px'; // Tamaño estándar de íconos.
const LATEST_ARTICLE_PLACEHOLDER = '%{{latest-article}}%'; // Placeholder para el último artículo.

(async () => {
  // Lee el template del README.
  const markdownTemplate = await fs.promises.readFile('./README.md.tpl', { encoding: 'utf-8' });

  // Obtiene los artículos del blog.
  const { items } = await parser.parseURL('https://jorgealexandervalencia.hashnode.dev/rss.xml');
  let latestArticle;

  // Determina el artículo más reciente.
  if (items.length > 8) {
    latestArticle = `[${items[0].title}](${items[0].link})`;
  } else {
    latestArticle = `[${items[7].title}](${items[7].link})`;
  }

  // Reemplaza placeholders en el template con valores reales.
  let newMarkdown = markdownTemplate.replace(LATEST_ARTICLE_PLACEHOLDER, latestArticle);
  newMarkdown = newMarkdown.replaceAll(ICONS_SIZE_PLACEHOLDER, ICON_SIZE);

  console.log(newMarkdown); // Imprime el resultado en la consola.
  await fs.promises.writeFile('./README.md', newMarkdown); // Actualiza el archivo README.
})();
