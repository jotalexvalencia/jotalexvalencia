const fs = require('fs').promises;
const Parser = require('rss-parser');
const parser = new Parser();

const ICONS_SIZE_PLACEHOLDER = '%{{icon_size}}%';
const ICON_SIZE = '24px';
const LATEST_ARTICLE_PLACEHOLDER = '%{{latest-article}}%';

(async () => {
   const markdownTemplate = await fs.readFile('./README.md.tpl', { encoding: 'utf-8' });  
   const {items} = await parser.parseURL('https://jorgealexandervalencia.hashnode.dev/rss.xml');
   const [{title, link}] = items;
   const latestArticleMarkdown = `[${title}](${link})`;

   // Primero, reemplaza el marcador de posición del último artículo
   let newMarkDowm = markdownTemplate.replace(LATEST_ARTICLE_PLACEHOLDER, latestArticleMarkdown);

   // Luego, reemplaza el marcador de posición del tamaño de los iconos en el resultado anterior
   newMarkDowm = newMarkDowm.replaceAll(ICONS_SIZE_PLACEHOLDER, ICON_SIZE);

   console.log(newMarkDowm);
   await fs.writeFile('./README.md', newMarkDowm);
})();
