function tratamento() {
	var cpfE = document.getElementById("cpf").value;
	var nomeE = document.getElementById("nome").value;
	var enderecoE = document.getElementById("endereco").value;
	var telefoneE = document.getElementById("telefone").value;
	var loginE = document.getElementById("login").value;
	var senhaE = document.getElementById("pwd").value;

	if (cpfE == "" || cpfE.length < 11){
		window.alert("Digite um cpf valido");
		return false;
	}

	if(nomeE == ""){
		window.alert("Digite seu nome completo");
		return false;
	}
	if(enderecoE == ""){
		window.alert("Digite um Enderço");
		return false;
	}

	if(telefoneE == ""){
		window.alert("Digite um telefone");
		return false;
	}

	if(loginE == ""){
		window.alert("Digite um login valido");
		return false;
	}

	if(senhaE == ""){
		window.alert("Digite uma senha valida");
		return false;
	}

}

