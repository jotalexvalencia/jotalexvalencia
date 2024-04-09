const fs = require('fs');
const Parser = require('rss-parser');
const parser = new Parser();

const ICONS_SIZE_PLACEHOLDER = '%{{icon_size}}%';
const ICON_SIZE = '24px';
const LATEST_ARTICLE_PLACEHOLDER = '%{{latest-article}}%';

(async () => {
   const markdownTemplate = await fs.promises.readFile('./README.md.tpl', { encoding: 'utf-8' });  
   const {items} = await parser.parseURL('https://jorgealexandervalencia.hashnode.dev/rss.xml');
   let latestArticle;

   if(items.length > 8) {
     latestArticle = `[${items[0].title}](${items[0].link})`; 
   } else {
     latestArticle = `[${items[7].title}](${items[7].link})`;
   }

   let newMarkdown = markdownTemplate.replace(LATEST_ARTICLE_PLACEHOLDER, latestArticle);
   newMarkdown = newMarkdown.replaceAll(ICONS_SIZE_PLACEHOLDER, ICON_SIZE);

   console.log(newMarkdown);
   await fs.promises.writeFile('./README.md', newMarkdown);
})();
