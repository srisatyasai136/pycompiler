let editor;

  require.config({
    paths: { 'vs': 'https://unpkg.com/monaco-editor@latest/min/vs' }
  });

  require(['vs/editor/editor.main'], function () {
    editor = monaco.editor.create(document.getElementById('editor'), {
      value: `#write your code here`,
      language: 'python',
      theme: 'vs-dark',
      automaticLayout: true
    });
  });

  async function runCode() {
    const code = editor.getValue();
    const input = document.getElementById('user_input').value;

    document.getElementById('run-text').style.display = 'none';
    document.getElementById('run-spinner').style.display = 'inline-block';
    document.getElementById('output').textContent = '';

    try {
      const res = await fetch('/run/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, input })
      });

      const data = await res.json();
      document.getElementById('output').textContent = data.output;
    } catch (err) {
      document.getElementById('output').textContent = '❌ Error running code';
    } finally {
      document.getElementById('run-text').style.display = 'inline';
      document.getElementById('run-spinner').style.display = 'none';
    }
  }