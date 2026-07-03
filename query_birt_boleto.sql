-- QUERY CONVERTIDA DE JASPERREPORTS PARA BIRT
-- Alterações principais:
-- 1. $P{CPF} → ? (placeholder BIRT)
-- 2. Mantém mesma lógica SQL

SELECT pes.nome,
       SUBSTR(lpad(p.cpf,11,0), 1, 3) || '.' ||
       SUBSTR(lpad(p.cpf,11,0), 4, 3) || '.' ||
       SUBSTR(lpad(p.cpf,11,0), 7, 3) || '-' ||
       SUBSTR(lpad(p.cpf,11,0), 10, 2) CPF,
       p.cep,
       p.endereco,
       p.bairro,
       p.cidade,
       p.uf,
       p.valor_solicitacao valor,
       TO_CHAR(p.data_vencimento, 'dd/mm/yyyy') data_vencimento,
       p.descricao,
       r.numerosolicitacao,
       r.pix_textoqrcode,
       SUBSTR(r.boleto_linhadigitavel, 1, 4) || '.' ||
       SUBSTR(r.boleto_linhadigitavel, 5, 5) || ' ' ||
       SUBSTR(r.boleto_linhadigitavel, 10, 5) || '.' ||
       SUBSTR(r.boleto_linhadigitavel, 15, 6) || ' ' ||
       SUBSTR(r.boleto_linhadigitavel, 21, 6) || ' ' ||
       SUBSTR(r.boleto_linhadigitavel, 27, 1) || ' ' ||
       SUBSTR(r.boleto_linhadigitavel, 28, 14) linha_digitavel,
       r.boleto_textocodigobarras,
       TO_CHAR(r.timestampcriacaosolicitacao, 'dd/mm/yyyy') data_solicitacao,
       p.codigo_conciliacao NrDocumento,
       to_char(r.timestampcriacaosolicitacao,'DD/MM/RRRR') data_processamento,
       lib_bb_api.NossoNumero(p.codigo_conciliacao) nosso_numero
  FROM bb_cobranca_pf p, bb_cobranca_pf_registrado r, pessoa pes
 WHERE p.status = 'T'
   AND r.id_bb_cobranca_pf = p.id
   AND pes.id = p.id_pessoa
   AND p.cpf = ?
