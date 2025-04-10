const fs = require('fs'); // Módulo para manejar operaciones de archivos en el sistema.
const Parser = require('rss-parser'); // Biblioteca para procesar feeds RSS.
const parser = new Parser();

const ICONS_SIZE_PLACEHOLDER = '%{{icon_size}}%'; // Placeholder para el tamaño de los íconos en la plantilla.
const ICON_SIZE = '24px'; // Tamaño predeterminado de los íconos.
const LATEST_ARTICLE_PLACEHOLDER = '%{{latest-article}}%'; // Placeholder para el último artículo.

(async () => {
  try {
    // Lee el archivo README.md.tpl, que es la plantilla para generar el README.md.
    const markdownTemplate = await fs.promises.readFile('./README.md.tpl', { encoding: 'utf-8' });

    // Intenta obtener los artículos del feed RSS de Hashnode.
    let items;
    try {
      const feed = await parser.parseURL('https://jorgealexandervalencia.hashnode.dev/rss.xml');
      items = feed.items || []; // Si no hay artículos, items será un arreglo vacío.
    } catch (error) {
      console.error('Error fetching RSS feed:', error.message);
      items = []; // Si hay un error al obtener el feed, asegura que items sea un arreglo vacío.
    }

    // Establece un artículo predeterminado si no hay artículos en el feed.
    const fallbackArticle = {
      title: 'Check out my portfolio and latest projects!', // Título predeterminado.
      link: 'https://jorgealexandervalenciavalenciadev.notion.site/', // Enlace predeterminado.
    };

    // Determina cuál artículo mostrar: el más reciente del feed o el predeterminado.
    const latestArticle = items.length > 0
      ? `[${items[0].title}](${items[0].link})` // Usa el primer artículo si hay datos disponibles.
      : `[${fallbackArticle.title}](${fallbackArticle.link})`; // Usa el artículo predeterminado si no hay datos.

    // Reemplaza los placeholders en la plantilla con la información generada.
    let newMarkdown = markdownTemplate.replace(LATEST_ARTICLE_PLACEHOLDER, latestArticle);
    newMarkdown = newMarkdown.replaceAll(ICONS_SIZE_PLACEHOLDER, ICON_SIZE);

    console.log('Generated README content:\n', newMarkdown); // Muestra el contenido generado en la consola.

    // Escribe el contenido generado en un archivo README.md.
    await fs.promises.writeFile('./README.md', newMarkdown);
    console.log('README.md file generated successfully!');
  } catch (error) {
    console.error('An error occurred:', error.message); // Muestra cualquier error inesperado.
  }
})();
