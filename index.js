const fs = require('fs').promises
const Parser = require('rss-parser');
const parser = new Parser();

const ICONS_SIZE_PLACEHOLDER = '%{{icon_size}}%';
const ICON_SIZE = '24px';


(async () => {
   const markdownTemplate = await fs.readFile('./README.md.tpl', { encoding: 'utf-8' } )   
   let newMarkDowm ;

   // put the icon size to all icons
   newMarkDowm = markdownTemplate.replaceAll(ICONS_SIZE_PLACEHOLDER, ICON_SIZE);
   await fs.writeFile('./README.md', newMarkDowm);
})()

    
   
