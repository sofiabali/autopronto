
fetch('/api/carros')
  .then(resp => resp.json())
  .then(data => {
    console.log("Carros disponíveis:", data);
  });
