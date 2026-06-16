import { useCallback, useEffect, useState } from 'react';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const CATEGORIAS = [
  { value: 'MEDICO', label: 'Medico' },
  { value: 'PSICOLOGO', label: 'Psicologo' },
  { value: 'FISIOTERAPEUTA', label: 'Fisioterapeuta' },
];

const TIPOS_RECEITA = [
  { value: 'REMEDIO', label: 'Remedio' },
  { value: 'ATIVIDADE_FISICA', label: 'Atividade fisica' },
  { value: 'ATIVIDADE_MENTAL', label: 'Atividade mental' },
];

const STATUS_ATENDIMENTO = [
  { value: 'AGENDADO', label: 'Agendado' },
  { value: 'REALIZADO', label: 'Realizado' },
  { value: 'CANCELADO', label: 'Cancelado' },
];

const profissionalInicial = { nome: '', telefone: '', endereco: '', categoria: 'MEDICO' };
const pacienteInicial = { nome: '', cpf: '', data_nascimento: '', telefone: '' };
const atendimentoInicial = {
  profissional_saude_id: '',
  paciente_id: '',
  data_atendimento: '',
  horario_atendimento: '',
  problema_texto: '',
  status: 'AGENDADO',
};
const receitaInicial = { atendimento_id: '', descricao: '', tipo: 'REMEDIO' };
const exameInicial = { atendimento_id: '', descricao: '' };
const prontuarioInicial = { atendimento_id: '', observacoes: '' };

function App() {
  const [aba, setAba] = useState('dashboard');
  const [loading, setLoading] = useState(false);
  const [profissionais, setProfissionais] = useState([]);
  const [pacientes, setPacientes] = useState([]);
  const [atendimentos, setAtendimentos] = useState([]);
  const [receitas, setReceitas] = useState([]);
  const [exames, setExames] = useState([]);
  const [prontuarios, setProntuarios] = useState([]);

  const [fProfissional, setFProfissional] = useState(profissionalInicial);
  const [fPaciente, setFPaciente] = useState(pacienteInicial);
  const [fAtendimento, setFAtendimento] = useState(atendimentoInicial);
  const [fReceita, setFReceita] = useState(receitaInicial);
  const [fExame, setFExame] = useState(exameInicial);
  const [fProntuario, setFProntuario] = useState(prontuarioInicial);

  const [editandoProfissionalId, setEditandoProfissionalId] = useState(null);
  const [editandoPacienteId, setEditandoPacienteId] = useState(null);
  const [editandoAtendimentoId, setEditandoAtendimentoId] = useState(null);
  const [editandoReceitaId, setEditandoReceitaId] = useState(null);
  const [editandoExameId, setEditandoExameId] = useState(null);
  const [editandoProntuarioId, setEditandoProntuarioId] = useState(null);

  const apiRequest = useCallback(async (endpoint, options = {}) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options,
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.detail || 'Nao foi possivel concluir a operacao');
    }

    if (response.status === 204) return null;
    return response.json();
  }, []);

  const carregarDados = useCallback(async () => {
    setLoading(true);
    try {
      const [
        profissionaisDados,
        pacientesDados,
        atendimentosDados,
        receitasDados,
        examesDados,
        prontuariosDados,
      ] = await Promise.all([
        apiRequest('/profissionais-saude/'),
        apiRequest('/pacientes/'),
        apiRequest('/atendimentos/'),
        apiRequest('/receitas-saude/'),
        apiRequest('/exames-lab/'),
        apiRequest('/prontuarios/'),
      ]);

      setProfissionais(profissionaisDados);
      setPacientes(pacientesDados);
      setAtendimentos(atendimentosDados);
      setReceitas(receitasDados);
      setExames(examesDados);
      setProntuarios(prontuariosDados);
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  }, [apiRequest]);

  useEffect(() => {
    carregarDados();
  }, [carregarDados]);

  const salvarRegistro = async ({
    endpoint,
    editandoId,
    payload,
    resetForm,
    limparEdicao,
    nomeEntidade,
  }) => {
    try {
      await apiRequest(editandoId ? `${endpoint}${editandoId}` : endpoint, {
        method: editandoId ? 'PUT' : 'POST',
        body: JSON.stringify(payload),
      });
      resetForm();
      limparEdicao(null);
      await carregarDados();
      alert(`${nomeEntidade} salvo com sucesso!`);
    } catch (error) {
      alert(error.message);
    }
  };

  const excluirRegistro = async (endpoint, id, nomeEntidade) => {
    if (!confirm(`Excluir ${nomeEntidade}?`)) return;

    try {
      await apiRequest(`${endpoint}${id}`, { method: 'DELETE' });
      await carregarDados();
    } catch (error) {
      alert(error.message);
    }
  };

  const handleTelefonePacienteChange = (event) => {
    setFPaciente({ ...fPaciente, telefone: aplicarMascaraTelefone(event.target.value) });
  };

  const handleTelefoneProfissionalChange = (event) => {
    setFProfissional({ ...fProfissional, telefone: aplicarMascaraTelefone(event.target.value) });
  };

  const iniciarEdicaoProfissional = (profissional) => {
    setEditandoProfissionalId(profissional.id);
    setFProfissional({
      nome: profissional.nome,
      telefone: profissional.telefone || '',
      endereco: profissional.endereco || '',
      categoria: profissional.categoria,
    });
  };

  const iniciarEdicaoPaciente = (paciente) => {
    setEditandoPacienteId(paciente.id);
    setFPaciente({
      nome: paciente.nome,
      cpf: paciente.cpf,
      data_nascimento: paciente.data_nascimento,
      telefone: paciente.telefone || '',
    });
  };

  const iniciarEdicaoAtendimento = (atendimento) => {
    setEditandoAtendimentoId(atendimento.id);
    setFAtendimento({
      profissional_saude_id: String(atendimento.profissional_saude_id),
      paciente_id: atendimento.paciente_id ? String(atendimento.paciente_id) : '',
      data_atendimento: atendimento.data_atendimento,
      horario_atendimento: atendimento.horario_atendimento.slice(0, 5),
      problema_texto: atendimento.problema_texto,
      status: atendimento.status,
    });
  };

  const iniciarEdicaoReceita = (receita) => {
    setEditandoReceitaId(receita.id);
    setFReceita({
      atendimento_id: String(receita.atendimento_id),
      descricao: receita.descricao,
      tipo: receita.tipo,
    });
  };

  const iniciarEdicaoExame = (exame) => {
    setEditandoExameId(exame.id);
    setFExame({
      atendimento_id: String(exame.atendimento_id),
      descricao: exame.descricao,
    });
  };

  const iniciarEdicaoProntuario = (prontuario) => {
    setEditandoProntuarioId(prontuario.id);
    setFProntuario({
      atendimento_id: String(prontuario.atendimento_id),
      observacoes: prontuario.observacoes,
    });
  };

  const salvarProfissional = (event) => {
    event.preventDefault();
    salvarRegistro({
      endpoint: '/profissionais-saude/',
      editandoId: editandoProfissionalId,
      payload: fProfissional,
      resetForm: () => setFProfissional(profissionalInicial),
      limparEdicao: setEditandoProfissionalId,
      nomeEntidade: 'Profissional de saude',
    });
  };

  const salvarPaciente = (event) => {
    event.preventDefault();
    salvarRegistro({
      endpoint: '/pacientes/',
      editandoId: editandoPacienteId,
      payload: fPaciente,
      resetForm: () => setFPaciente(pacienteInicial),
      limparEdicao: setEditandoPacienteId,
      nomeEntidade: 'Paciente',
    });
  };

  const salvarAtendimento = (event) => {
    event.preventDefault();
    salvarRegistro({
      endpoint: '/atendimentos/',
      editandoId: editandoAtendimentoId,
      payload: {
        ...fAtendimento,
        profissional_saude_id: Number(fAtendimento.profissional_saude_id),
        paciente_id: fAtendimento.paciente_id ? Number(fAtendimento.paciente_id) : null,
      },
      resetForm: () => setFAtendimento(atendimentoInicial),
      limparEdicao: setEditandoAtendimentoId,
      nomeEntidade: 'Atendimento',
    });
  };

  const salvarReceita = (event) => {
    event.preventDefault();
    salvarRegistro({
      endpoint: '/receitas-saude/',
      editandoId: editandoReceitaId,
      payload: { ...fReceita, atendimento_id: Number(fReceita.atendimento_id) },
      resetForm: () => setFReceita(receitaInicial),
      limparEdicao: setEditandoReceitaId,
      nomeEntidade: 'Receita de saude',
    });
  };

  const salvarExame = (event) => {
    event.preventDefault();
    salvarRegistro({
      endpoint: '/exames-lab/',
      editandoId: editandoExameId,
      payload: { ...fExame, atendimento_id: Number(fExame.atendimento_id) },
      resetForm: () => setFExame(exameInicial),
      limparEdicao: setEditandoExameId,
      nomeEntidade: 'Exame laboratorial',
    });
  };

  const salvarProntuario = (event) => {
    event.preventDefault();
    salvarRegistro({
      endpoint: '/prontuarios/',
      editandoId: editandoProntuarioId,
      payload: { ...fProntuario, atendimento_id: Number(fProntuario.atendimento_id) },
      resetForm: () => setFProntuario(prontuarioInicial),
      limparEdicao: setEditandoProntuarioId,
      nomeEntidade: 'Prontuario',
    });
  };

  const renderSelectOptions = (opcoes) => opcoes.map((opcao) => (
    <option key={opcao.value} value={opcao.value}>{opcao.label}</option>
  ));

  const renderAtendimentoOptions = () => atendimentos.map((atendimento) => (
    <option key={atendimento.id} value={atendimento.id}>
      {formatarAtendimento(atendimento)}
    </option>
  ));

  return (
    <div>
      <nav className="navbar">
        <div className="nav-brand">HEALTHCARE SYSTEM · PUC Minas</div>
        <div className="nav-links">
          <button className={`nav-btn ${aba === 'dashboard' ? 'active' : ''}`} onClick={() => setAba('dashboard')}>Dashboard</button>
          <button className={`nav-btn ${aba === 'profissionais' ? 'active' : ''}`} onClick={() => setAba('profissionais')}>Profissionais</button>
          <button className={`nav-btn ${aba === 'pacientes' ? 'active' : ''}`} onClick={() => setAba('pacientes')}>Pacientes</button>
          <button className={`nav-btn ${aba === 'atendimentos' ? 'active' : ''}`} onClick={() => setAba('atendimentos')}>Atendimentos</button>
          <button className={`nav-btn ${aba === 'receitas' ? 'active' : ''}`} onClick={() => setAba('receitas')}>Receitas</button>
          <button className={`nav-btn ${aba === 'exames' ? 'active' : ''}`} onClick={() => setAba('exames')}>Exames</button>
          <button className={`nav-btn ${aba === 'prontuarios' ? 'active' : ''}`} onClick={() => setAba('prontuarios')}>Prontuarios</button>
        </div>
      </nav>

      <div className="container">
        {loading && <div className="loading-bar">Atualizando dados...</div>}

        {aba === 'dashboard' && (
          <>
            <h2 className="page-title">Resumo da Clinica</h2>
            <div className="stats-row">
              <StatCard label="Profissionais" value={profissionais.length} />
              <StatCard label="Pacientes" value={pacientes.length} />
              <StatCard label="Atendimentos" value={atendimentos.length} />
              <StatCard label="Receitas" value={receitas.length} />
              <StatCard label="Exames" value={exames.length} />
              <StatCard label="Prontuarios" value={prontuarios.length} />
            </div>
            <div className="card">
              <h3 className="card-title">Atendimentos Recentes</h3>
              <TabelaAtendimentos atendimentos={atendimentos.slice(0, 5)} />
            </div>
          </>
        )}

        {aba === 'profissionais' && (
          <>
            <h2 className="page-title">Profissionais de Saude</h2>
            <div className="card">
              <h3 className="card-title">{editandoProfissionalId ? 'Editar Profissional' : 'Cadastrar Profissional'}</h3>
              <form onSubmit={salvarProfissional}>
                <div className="form-grid">
                  <CampoTexto label="Nome" value={fProfissional.nome} onChange={(valor) => setFProfissional({ ...fProfissional, nome: valor })} required />
                  <CampoTexto label="Telefone" value={fProfissional.telefone} onChange={(_, event) => handleTelefoneProfissionalChange(event)} />
                  <CampoTexto label="Endereco" value={fProfissional.endereco} onChange={(valor) => setFProfissional({ ...fProfissional, endereco: valor })} />
                  <div className="form-group">
                    <label>Categoria</label>
                    <select value={fProfissional.categoria} onChange={(e) => setFProfissional({ ...fProfissional, categoria: e.target.value })}>
                      {renderSelectOptions(CATEGORIAS)}
                    </select>
                  </div>
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn-submit">{editandoProfissionalId ? 'Atualizar' : 'Salvar'} Profissional</button>
                  {editandoProfissionalId && (
                    <button type="button" className="btn-secondary" onClick={() => { setEditandoProfissionalId(null); setFProfissional(profissionalInicial); }}>Cancelar</button>
                  )}
                </div>
              </form>
            </div>
            <div className="card">
              <h3 className="card-title">Profissionais Cadastrados</h3>
              <div className="table-wrapper">
                <table>
                  <thead><tr><th>Nome</th><th>Telefone</th><th>Endereco</th><th>Categoria</th><th>Acoes</th></tr></thead>
                  <tbody>
                    {profissionais.map((profissional) => (
                      <tr key={profissional.id}>
                        <td>{profissional.nome}</td>
                        <td>{profissional.telefone || '-'}</td>
                        <td>{profissional.endereco || '-'}</td>
                        <td><span className="badge">{profissional.categoria}</span></td>
                        <td>
                          <TableActions
                            onEdit={() => iniciarEdicaoProfissional(profissional)}
                            onDelete={() => excluirRegistro('/profissionais-saude/', profissional.id, 'profissional')}
                          />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}

        {aba === 'pacientes' && (
          <>
            <h2 className="page-title">Pacientes</h2>
            <div className="card">
              <h3 className="card-title">{editandoPacienteId ? 'Editar Paciente' : 'Cadastrar Paciente'}</h3>
              <form onSubmit={salvarPaciente}>
                <div className="form-grid">
                  <CampoTexto label="Nome Completo" value={fPaciente.nome} onChange={(valor) => setFPaciente({ ...fPaciente, nome: valor })} required />
                  <CampoTexto label="CPF" value={fPaciente.cpf} onChange={(valor) => setFPaciente({ ...fPaciente, cpf: valor })} required />
                  <CampoTexto label="Data de Nascimento" type="date" value={fPaciente.data_nascimento} onChange={(valor) => setFPaciente({ ...fPaciente, data_nascimento: valor })} required />
                  <CampoTexto label="Telefone" value={fPaciente.telefone} onChange={(_, event) => handleTelefonePacienteChange(event)} />
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn-submit">{editandoPacienteId ? 'Atualizar' : 'Salvar'} Paciente</button>
                  {editandoPacienteId && (
                    <button type="button" className="btn-secondary" onClick={() => { setEditandoPacienteId(null); setFPaciente(pacienteInicial); }}>Cancelar</button>
                  )}
                </div>
              </form>
            </div>
            <div className="card">
              <h3 className="card-title">Pacientes Cadastrados</h3>
              <div className="table-wrapper">
                <table>
                  <thead><tr><th>Nome</th><th>CPF</th><th>Nascimento</th><th>Telefone</th><th>Acoes</th></tr></thead>
                  <tbody>
                    {pacientes.map((paciente) => (
                      <tr key={paciente.id}>
                        <td>{paciente.nome}</td>
                        <td>{paciente.cpf}</td>
                        <td>{formatarData(paciente.data_nascimento)}</td>
                        <td>{paciente.telefone || '-'}</td>
                        <td>
                          <TableActions
                            onEdit={() => iniciarEdicaoPaciente(paciente)}
                            onDelete={() => excluirRegistro('/pacientes/', paciente.id, 'paciente')}
                          />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}

        {aba === 'atendimentos' && (
          <>
            <h2 className="page-title">Atendimentos</h2>
            <div className="card">
              <h3 className="card-title">{editandoAtendimentoId ? 'Editar Atendimento' : 'Novo Atendimento'}</h3>
              <form onSubmit={salvarAtendimento}>
                <div className="form-grid">
                  <div className="form-group">
                    <label>Profissional</label>
                    <select value={fAtendimento.profissional_saude_id} onChange={(e) => setFAtendimento({ ...fAtendimento, profissional_saude_id: e.target.value })} required>
                      <option value="">Selecione...</option>
                      {profissionais.map((profissional) => (
                        <option key={profissional.id} value={profissional.id}>{profissional.nome} - {profissional.categoria}</option>
                      ))}
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Paciente</label>
                    <select value={fAtendimento.paciente_id} onChange={(e) => setFAtendimento({ ...fAtendimento, paciente_id: e.target.value })}>
                      <option value="">Sem paciente vinculado</option>
                      {pacientes.map((paciente) => (
                        <option key={paciente.id} value={paciente.id}>{paciente.nome}</option>
                      ))}
                    </select>
                  </div>
                  <CampoTexto label="Data" type="date" value={fAtendimento.data_atendimento} onChange={(valor) => setFAtendimento({ ...fAtendimento, data_atendimento: valor })} required />
                  <CampoTexto label="Horario" type="time" value={fAtendimento.horario_atendimento} onChange={(valor) => setFAtendimento({ ...fAtendimento, horario_atendimento: valor })} required />
                  <div className="form-group">
                    <label>Status</label>
                    <select value={fAtendimento.status} onChange={(e) => setFAtendimento({ ...fAtendimento, status: e.target.value })}>
                      {renderSelectOptions(STATUS_ATENDIMENTO)}
                    </select>
                  </div>
                </div>
                <div className="form-group field-full">
                  <label>Problema / descricao do atendimento</label>
                  <textarea rows="4" value={fAtendimento.problema_texto} onChange={(e) => setFAtendimento({ ...fAtendimento, problema_texto: e.target.value })} required />
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn-submit">{editandoAtendimentoId ? 'Atualizar' : 'Salvar'} Atendimento</button>
                  {editandoAtendimentoId && (
                    <button type="button" className="btn-secondary" onClick={() => { setEditandoAtendimentoId(null); setFAtendimento(atendimentoInicial); }}>Cancelar</button>
                  )}
                </div>
              </form>
            </div>
            <div className="card">
              <h3 className="card-title">Atendimentos Cadastrados</h3>
              <TabelaAtendimentos
                atendimentos={atendimentos}
                onEdit={iniciarEdicaoAtendimento}
                onDelete={(atendimento) => excluirRegistro('/atendimentos/', atendimento.id, 'atendimento')}
              />
            </div>
          </>
        )}

        {aba === 'receitas' && (
          <>
            <h2 className="page-title">Receitas de Saude</h2>
            <div className="card">
              <h3 className="card-title">{editandoReceitaId ? 'Editar Receita' : 'Cadastrar Receita'}</h3>
              <form onSubmit={salvarReceita}>
                <div className="form-grid">
                  <div className="form-group">
                    <label>Atendimento</label>
                    <select value={fReceita.atendimento_id} onChange={(e) => setFReceita({ ...fReceita, atendimento_id: e.target.value })} required>
                      <option value="">Selecione...</option>
                      {renderAtendimentoOptions()}
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Tipo</label>
                    <select value={fReceita.tipo} onChange={(e) => setFReceita({ ...fReceita, tipo: e.target.value })}>
                      {renderSelectOptions(TIPOS_RECEITA)}
                    </select>
                  </div>
                </div>
                <div className="form-group field-full">
                  <label>Descricao</label>
                  <textarea rows="4" value={fReceita.descricao} onChange={(e) => setFReceita({ ...fReceita, descricao: e.target.value })} required />
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn-submit">{editandoReceitaId ? 'Atualizar' : 'Salvar'} Receita</button>
                  {editandoReceitaId && (
                    <button type="button" className="btn-secondary" onClick={() => { setEditandoReceitaId(null); setFReceita(receitaInicial); }}>Cancelar</button>
                  )}
                </div>
              </form>
            </div>
            <RegistroSimplesTable
              titulo="Receitas Cadastradas"
              registros={receitas}
              atendimentos={atendimentos}
              campoDescricao="descricao"
              campoExtra="tipo"
              onEdit={iniciarEdicaoReceita}
              onDelete={(receita) => excluirRegistro('/receitas-saude/', receita.id, 'receita')}
            />
          </>
        )}

        {aba === 'exames' && (
          <>
            <h2 className="page-title">Exames Laboratoriais</h2>
            <div className="card">
              <h3 className="card-title">{editandoExameId ? 'Editar Exame' : 'Cadastrar Exame'}</h3>
              <form onSubmit={salvarExame}>
                <div className="form-grid">
                  <div className="form-group">
                    <label>Atendimento</label>
                    <select value={fExame.atendimento_id} onChange={(e) => setFExame({ ...fExame, atendimento_id: e.target.value })} required>
                      <option value="">Selecione...</option>
                      {renderAtendimentoOptions()}
                    </select>
                  </div>
                </div>
                <div className="form-group field-full">
                  <label>Descricao</label>
                  <textarea rows="4" value={fExame.descricao} onChange={(e) => setFExame({ ...fExame, descricao: e.target.value })} required />
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn-submit">{editandoExameId ? 'Atualizar' : 'Salvar'} Exame</button>
                  {editandoExameId && (
                    <button type="button" className="btn-secondary" onClick={() => { setEditandoExameId(null); setFExame(exameInicial); }}>Cancelar</button>
                  )}
                </div>
              </form>
            </div>
            <RegistroSimplesTable
              titulo="Exames Cadastrados"
              registros={exames}
              atendimentos={atendimentos}
              campoDescricao="descricao"
              onEdit={iniciarEdicaoExame}
              onDelete={(exame) => excluirRegistro('/exames-lab/', exame.id, 'exame')}
            />
          </>
        )}

        {aba === 'prontuarios' && (
          <>
            <h2 className="page-title">Prontuarios</h2>
            <div className="card">
              <h3 className="card-title">{editandoProntuarioId ? 'Editar Prontuario' : 'Registrar Prontuario'}</h3>
              <form onSubmit={salvarProntuario}>
                <div className="form-grid">
                  <div className="form-group">
                    <label>Atendimento</label>
                    <select value={fProntuario.atendimento_id} onChange={(e) => setFProntuario({ ...fProntuario, atendimento_id: e.target.value })} required>
                      <option value="">Selecione...</option>
                      {renderAtendimentoOptions()}
                    </select>
                  </div>
                </div>
                <div className="form-group field-full">
                  <label>Observacoes</label>
                  <textarea rows="5" value={fProntuario.observacoes} onChange={(e) => setFProntuario({ ...fProntuario, observacoes: e.target.value })} required />
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn-submit">{editandoProntuarioId ? 'Atualizar' : 'Salvar'} Prontuario</button>
                  {editandoProntuarioId && (
                    <button type="button" className="btn-secondary" onClick={() => { setEditandoProntuarioId(null); setFProntuario(prontuarioInicial); }}>Cancelar</button>
                  )}
                </div>
              </form>
            </div>
            <RegistroSimplesTable
              titulo="Prontuarios Cadastrados"
              registros={prontuarios}
              atendimentos={atendimentos}
              campoDescricao="observacoes"
              campoExtra="data_criacao"
              onEdit={iniciarEdicaoProntuario}
              onDelete={(prontuario) => excluirRegistro('/prontuarios/', prontuario.id, 'prontuario')}
            />
          </>
        )}
      </div>
    </div>
  );
}

function aplicarMascaraTelefone(valorEntrada) {
  let valor = valorEntrada.replace(/\D/g, '');
  if (valor.length > 11) valor = valor.slice(0, 11);
  if (valor.length > 2) valor = `(${valor.slice(0, 2)}) ${valor.slice(2)}`;
  if (valor.length > 9) valor = `${valor.slice(0, 10)}-${valor.slice(10)}`;
  return valor;
}

function CampoTexto({ label, value, onChange, type = 'text', required = false }) {
  return (
    <div className="form-group">
      <label>{label}</label>
      <input type={type} value={value} onChange={(event) => onChange(event.target.value, event)} required={required} />
    </div>
  );
}

function StatCard({ label, value }) {
  return (
    <div className="stat-card">
      <div className="stat-label">{label}</div>
      <div className="stat-number">{value}</div>
    </div>
  );
}

function TableActions({ onEdit, onDelete }) {
  return (
    <div className="table-actions">
      <button type="button" className="btn-small" onClick={onEdit}>Editar</button>
      <button type="button" className="btn-small btn-danger" onClick={onDelete}>Excluir</button>
    </div>
  );
}

function TabelaAtendimentos({ atendimentos, onEdit, onDelete }) {
  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Profissional</th>
            <th>Paciente</th>
            <th>Data</th>
            <th>Horario</th>
            <th>Status</th>
            {(onEdit || onDelete) && <th>Acoes</th>}
          </tr>
        </thead>
        <tbody>
          {atendimentos.map((atendimento) => (
            <tr key={atendimento.id}>
              <td>{atendimento.profissional_saude?.nome || '-'}</td>
              <td>{atendimento.paciente?.nome || '-'}</td>
              <td>{formatarData(atendimento.data_atendimento)}</td>
              <td>{atendimento.horario_atendimento?.slice(0, 5)}</td>
              <td><span className="badge">{atendimento.status}</span></td>
              {(onEdit || onDelete) && (
                <td>
                  <TableActions
                    onEdit={() => onEdit(atendimento)}
                    onDelete={() => onDelete(atendimento)}
                  />
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function RegistroSimplesTable({
  titulo,
  registros,
  atendimentos,
  campoDescricao,
  campoExtra,
  onEdit,
  onDelete,
}) {
  return (
    <div className="card">
      <h3 className="card-title">{titulo}</h3>
      <div className="table-wrapper">
        <table>
          <thead><tr><th>Atendimento</th><th>Descricao</th>{campoExtra && <th>Info</th>}<th>Acoes</th></tr></thead>
          <tbody>
            {registros.map((registro) => (
              <tr key={registro.id}>
                <td>{formatarAtendimento(atendimentos.find((atendimento) => atendimento.id === registro.atendimento_id))}</td>
                <td>{registro[campoDescricao]}</td>
                {campoExtra && <td>{campoExtra === 'data_criacao' ? formatarDataHora(registro[campoExtra]) : registro[campoExtra]}</td>}
                <td>
                  <TableActions
                    onEdit={() => onEdit(registro)}
                    onDelete={() => onDelete(registro)}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function formatarAtendimento(atendimento) {
  if (!atendimento) return '-';
  return `#${atendimento.id} - ${formatarData(atendimento.data_atendimento)} ${atendimento.horario_atendimento?.slice(0, 5)} - ${atendimento.profissional_saude?.nome || 'Sem profissional'}`;
}

function formatarData(valor) {
  if (!valor) return '-';
  return new Date(`${valor}T00:00:00`).toLocaleDateString('pt-BR');
}

function formatarDataHora(valor) {
  if (!valor) return '-';
  return new Date(valor).toLocaleString('pt-BR');
}

export default App;
