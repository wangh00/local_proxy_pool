const fs = require('fs');
const jsyaml = require('js-yaml');
// 读取文本文件
function get_file() {
  try {
    const data = fs.readFileSync('clash_proxy/before_conversion.txt', 'utf-8');
    // console.log('File content:', data);
    return data;
  } catch (err) {
    console.error('Error reading file:', err);
    return '';
  }
}
function saveToYAMLFile(content, filename) {
  try {
    const yamlContent = jsyaml.dump(content);
    fs.writeFileSync(filename, yamlContent, 'utf-8');
    console.log(`File '${filename}' saved successfully.`);
  } catch (err) {
    console.error('Error saving file:', err);
  }
}

function get_clash_demo() {
    const inputYAML=get_file()
    const yamlData = jsyaml.load(inputYAML);
    // console.log(yamlData)
    const startPort=42000
    const numProxies = yamlData.proxies.length;
    const newYAML = {
        'allow-lan': true,
        dns: {
            enable: true,
            'enhanced-mode': 'fake-ip',
            'fake-ip-range': '198.18.0.1/16',
            'default-nameserver': ['114.114.114.114'],
            nameserver: ['https://doh.pub/dns-query']
        },
        listeners: [],
        proxies: yamlData.proxies
    };
    newYAML.listeners = Array.from({
        length: numProxies
    },
    (_, i) => ({
        name: `mixed`+i,
        type: 'mixed',
        port: startPort + i,
        proxy: yamlData.proxies[i].name
    }));
    // const newYAMLString = jsyaml.dump(newYAML);
    const newYAMLString = newYAML;
    console.log(newYAMLString)
    return newYAMLString
}


clash_demo=get_clash_demo()
saveToYAMLFile(clash_demo, 'config.yaml');
// saveToYAMLFile(clash_demo, 'clash_proxy/config.yaml');
// saveToYAMLFile(clash_demo, 'socks_program/config1.yaml');

