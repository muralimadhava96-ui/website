const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const DOCS_DIR = path.resolve(__dirname, '../');

function getMarkdownFiles(dir) {
  let results = [];
  const files = fs.readdirSync(dir);

  files.forEach((file) => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);

    if (stat && stat.isDirectory()) {
      // skip node_modules and .git
      if (file === 'node_modules' || file === '.git') return;
      results = results.concat(getMarkdownFiles(fullPath));
    } else if (file.endsWith('.md') || file.endsWith('.mdx')) {
      results.push(fullPath);
    }
  });

  return results;
}

async function checkLinks() {
  const files = getMarkdownFiles(DOCS_DIR);

  for (const file of files) {
    console.log(`Checking: ${file}`);
    await new Promise((resolve, reject) => {
      exec(`npx markdown-link-check "${file}"`, (err, stdout, stderr) => {
        process.stdout.write(stdout || '');
        process.stderr.write(stderr || '');
        if (err) reject(err);
        else resolve();
      });
    });
  }
}

checkLinks().catch((err) => {
  console.error('Broken links detected');
  console.error(err && err.message ? err.message : err);
  process.exit(1);
});
