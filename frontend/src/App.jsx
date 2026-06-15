import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = "http://localhost:8000/api";

function App() {
  const [aba, setAba] = useState('dashboard');
  const [pacientes, setPacientes] = useState([]);
  const [medicos, setMedicos] = useState([]);
  const [agendamentos, setAgendamentos] = useState([]);

  // Estados dos formulários
  const [fPaciente, setFPaciente] = useState({ nome: '', cpf: '', data_nascimento: '', telefone: '' });
  const [fMedico, setFMedico] = useState({ nome: '', crm: '', especialidade: '' });
  const [fAgendamento, setFAgendamento] = useState({ paciente_id: '', medico_id: '', data_hora: '', status: 'Agendado' });
  const [fProntuario, setFProntuario] = useState({ agendamento_id: '', observacoes: '' });

  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = () => {
    fetch(`${API_URL}/pacientes/`).then(r => r.json()).then(setPacientes);
    fetch(`${API_URL}/medicos/`).then(r => r.json()).then(setMedicos);
    fetch(`${API_URL}/agendamentos/`).then(r => r.json()).then(setAgendamentos);
  };

  const enviarForm = (endpoint, data, resetFunc) => {
    fetch(`${API_URL}/${endpoint}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(res => {
      if(res.ok) {
        carregarDados();
        resetFunc();
        alert("Salvo com sucesso!");
      } else {
        res.json().then(err => alert("Erro: " + err.detail));
      }
    });
  };

  // Função para aplicar máscara de telefone (XX) 9XXXX-XXXX
  const handleTelefoneChange = (e) => {
    let valor = e.target.value.replace(/\D/g, ""); // Remove tudo que não é número
    
    if (valor.length > 11) valor = valor.slice(0, 11); // Limita a 11 números

    // Aplica a máscara (XX) 9XXXX-XXXX
    if (valor.length > 2) {
      valor = `(${valor.slice(0, 2)}) ${valor.slice(2)}`;
    }
    if (valor.length > 9) {
      valor = `${valor.slice(0, 10)}-${valor.slice(10)}`;
    }

    setFPaciente({ ...fPaciente, telefone: valor });
  };

  return (
    <div>
      {/* BARRA DE NAVEGAÇÃO */}
      <nav className="navbar">
        <div className="nav-brand">HEALTHCARE SYSTEM</div>
        <div className="nav-links">
          <button className={`nav-btn ${aba === 'dashboard' ? 'active' : ''}`} onClick={() => setAba('dashboard')}>Dashboard</button>
          <button className={`nav-btn ${aba === 'pacientes' ? 'active' : ''}`} onClick={() => setAba('pacientes')}>Pacientes</button>
          <button className={`nav-btn ${aba === 'medicos' ? 'active' : ''}`} onClick={() => setAba('medicos')}>Médicos</button>
          <button className={`nav-btn ${aba === 'agendamentos' ? 'active' : ''}`} onClick={() => setAba('agendamentos')}>Agenda</button>
          <button className={`nav-btn ${aba === 'prontuarios' ? 'active' : ''}`} onClick={() => setAba('prontuarios')}>Prontuários</button>
        </div>
      </nav>

      <div className="container">
        
        {/* CONTEÚDO: DASHBOARD */}
        {aba === 'dashboard' && (
          <>
            <h2 className="page-title">Resumo da Clínica</h2>
            <div className="stats-row">
              <div className="stat-card">
                <div className="stat-label">Total de Pacientes</div>
                <div className="stat-number">{pacientes.length}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Total de Médicos</div>
                <div className="stat-number">{medicos.length}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Agendamentos Ativos</div>
                <div className="stat-number">{agendamentos.length}</div>
              </div>
            </div>
            <div className="card">
              <h3 className="card-title">Consultas Recentes</h3>
              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr><th>Paciente</th><th>Médico</th><th>Data e Hora</th><th>Status</th></tr>
                  </thead>
                  <tbody>
                    {agendamentos.slice(-5).reverse().map(a => (
                      <tr key={a.id}>
                        <td>{a.paciente.nome}</td>
                        <td>{a.medico.nome}</td>
                        <td>{new Date(a.data_hora).toLocaleString()}</td>
                        <td><span className="badge">{a.status}</span></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}

        {/* CONTEÚDO: PACIENTES */}
        {aba === 'pacientes' && (
          <>
            <h2 className="page-title">Gerenciamento de Pacientes</h2>
            <div className="card">
              <h3 className="card-title">Cadastrar Paciente</h3>
              <form onSubmit={e => { e.preventDefault(); enviarForm('pacientes', fPaciente, () => setFPaciente({nome:'', cpf:'', data_nascimento:'', telefone:''})) }}>
                <div className="form-grid">
                  <div className="form-group">
                    <label>Nome Completo</label>
                    <input value={fPaciente.nome} onChange={e => setFPaciente({...fPaciente, nome: e.target.value})} required />
                  </div>
                  <div className="form-group">
                    <label>CPF</label>
                    <input value={fPaciente.cpf} onChange={e => setFPaciente({...fPaciente, cpf: e.target.value})} required />
                  </div>
                  <div className="form-group">
                    <label>Data de Nascimento</label>
                    <input type="date" value={fPaciente.data_nascimento} onChange={e => setFPaciente({...fPaciente, data_nascimento: e.target.value})} required />
                  </div>
                  <div className="form-group">
                    <label>Telefone</label>
                    <input 
                      placeholder="(XX) 9XXXX-XXXX"
                      value={fPaciente.telefone} 
                      onChange={handleTelefoneChange} 
                    />
                  </div>
                </div>
                <button type="submit" className="btn-submit">Salvar Paciente</button>
              </form>
            </div>
            <div className="card">
              <h3 className="card-title">Pacientes Cadastrados</h3>
              <div className="table-wrapper">
                <table>
                  <thead><tr><th>Nome</th><th>CPF</th><th>Telefone</th></tr></thead>
                  <tbody>
                    {pacientes.map(p => <tr key={p.id}><td>{p.nome}</td><td>{p.cpf}</td><td>{p.telefone}</td></tr>)}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}

        {/* CONTEÚDO: MÉDICOS */}
        {aba === 'medicos' && (
          <>
            <h2 className="page-title">Corpo Clínico</h2>
            <div className="card">
              <h3 className="card-title">Adicionar Médico</h3>
              <form onSubmit={e => { e.preventDefault(); enviarForm('medicos', fMedico, () => setFMedico({nome:'', crm:'', especialidade:''})) }}>
                <div className="form-grid">
                  <div className="form-group">
                    <label>Nome do Médico</label>
                    <input value={fMedico.nome} onChange={e => setFMedico({...fMedico, nome: e.target.value})} required />
                  </div>
                  <div className="form-group">
                    <label>CRM</label>
                    <input value={fMedico.crm} onChange={e => setFMedico({...fMedico, crm: e.target.value})} required />
                  </div>
                  <div className="form-group">
                    <label>Especialidade</label>
                    <input value={fMedico.especialidade} onChange={e => setFMedico({...fMedico, especialidade: e.target.value})} required />
                  </div>
                </div>
                <button type="submit" className="btn-submit">Cadastrar Médico</button>
              </form>
            </div>
            <div className="card">
              <h3 className="card-title">Lista de Médicos</h3>
              <div className="table-wrapper">
                <table>
                  <thead><tr><th>Nome</th><th>CRM</th><th>Especialidade</th></tr></thead>
                  <tbody>
                    {medicos.map(m => <tr key={m.id}><td>{m.nome}</td><td>{m.crm}</td><td>{m.especialidade}</td></tr>)}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}

        {/* CONTEÚDO: AGENDAMENTOS */}
        {aba === 'agendamentos' && (
          <>
            <h2 className="page-title">Agenda de Consultas</h2>
            <div className="card">
              <h3 className="card-title">Novo Agendamento</h3>
              <form onSubmit={e => { e.preventDefault(); enviarForm('agendamentos', fAgendamento, () => setFAgendamento({paciente_id:'', medico_id:'', data_hora:'', status:'Agendado'})) }}>
                <div className="form-grid">
                  <div className="form-group">
                    <label>Paciente</label>
                    <select value={fAgendamento.paciente_id} onChange={e => setFAgendamento({...fAgendamento, paciente_id: e.target.value})} required>
                      <option value="">Selecione o paciente...</option>
                      {pacientes.map(p => <option key={p.id} value={p.id}>{p.nome}</option>)}
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Médico</label>
                    <select value={fAgendamento.medico_id} onChange={e => setFAgendamento({...fAgendamento, medico_id: e.target.value})} required>
                      <option value="">Selecione o médico...</option>
                      {medicos.map(m => <option key={m.id} value={m.id}>{m.nome} - {m.especialidade}</option>)}
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Data e Horário</label>
                    <input type="datetime-local" value={fAgendamento.data_hora} onChange={e => setFAgendamento({...fAgendamento, data_hora: e.target.value})} required />
                  </div>
                </div>
                <button type="submit" className="btn-submit">Marcar Consulta</button>
              </form>
            </div>
            <div className="card">
              <h3 className="card-title">Consultas Agendadas</h3>
              <div className="table-wrapper">
                <table>
                  <thead><tr><th>Paciente</th><th>Médico</th><th>Horário</th><th>Status</th></tr></thead>
                  <tbody>
                    {agendamentos.map(a => (
                      <tr key={a.id}>
                        <td>{a.paciente.nome}</td>
                        <td>{a.medico.nome}</td>
                        <td>{new Date(a.data_hora).toLocaleString()}</td>
                        <td><span className="badge">{a.status}</span></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}

        {aba === 'prontuarios' && (
          <>
            <h2 className="page-title">Prontuário de Atendimento</h2>
            <div className="card">
              <h3 className="card-title">Registrar Atendimento</h3>
              <form onSubmit={e => { e.preventDefault(); enviarForm('prontuarios', fProntuario, () => setFProntuario({agendamento_id:'', observacoes:''})) }}>
                <div className="form-group" style={{marginBottom:'1rem'}}>
                  <label>Selecione a Consulta (Paciente - Data)</label>
                  <select value={fProntuario.agendamento_id} onChange={e => setFProntuario({...fProntuario, agendamento_id: e.target.value})} required>
                    <option value="">Escolha uma consulta...</option>
                    {agendamentos.map(a => (
                      <option key={a.id} value={a.id}>{a.paciente.nome} ({new Date(a.data_hora).toLocaleDateString()})</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Observações do Médico</label>
                  <textarea rows="5" value={fProntuario.observacoes} onChange={e => setFProntuario({...fProntuario, observacoes: e.target.value})} placeholder="Escreva aqui o diagnóstico e prescrições..." required></textarea>
                </div>
                <button type="submit" className="btn-submit">Finalizar Atendimento</button>
              </form>
            </div>
          </>
        )}

      </div>
    </div>
  );
}

export default App;
