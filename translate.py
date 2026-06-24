# -*- coding: utf-8 -*-
import re, html

BASE = "C:/Users/roger/Desktop/Projetos/Teste-Croche/artes-cristas-copia/index.html"

T = {
 "Artes Cristas – arquivoscnc.online": "Artes Cristianas – arquivoscnc.online",
 "⚡ ACESSO PROMOCIONAL LIBERADO HOJE 20/06/2026": "⚡ ACCESO PROMOCIONAL LIBERADO HOY 20/06/2026",
 "🔒 ACESSO 100% SEGURO E IMEDIATO": "🔒 ACCESO 100% SEGURO E INMEDIATO",
 "+50 ARTES CRISTÃS PREMIUM PRONTAS PARA CNC E LASER": "+50 ARTES CRISTIANAS PREMIUM LISTAS PARA CNC Y LÁSER",
 "Escolha o modelo, baixe na hora e produza peças cristãs profissionais na sua CNC ou laser.": "Elige el modelo, descárgalo al instante y produce piezas cristianas profesionales en tu CNC o láser.",
 "Compatível com Aspire, ArtCAM e Laser": "Compatible con Aspire, ArtCAM y Láser",
 "Arquivos testados e prontos para corte": "Archivos probados y listos para cortar",
 "Produza sem criar arte do zero": "Produce sin crear arte desde cero",
 "ACESSAR AGORA": "ACCEDER AHORA",
 "Você recebe tudo na hora, direto no seu": "Recibes todo al instante, directo en tu",
 "e-mail": "correo",
 "VEJA COMO SUAS PEÇAS PODEM FICAR": "MIRA CÓMO PUEDEN QUEDAR TUS PIEZAS",
 "Tudo o que você precisa já está pronto para usar na sua CNC ou laser.": "Todo lo que necesitas ya está listo para usar en tu CNC o láser.",
 "baixa": "descarga",
 "corta": "corta",
 "vende": "vende",
 "QUERO AS ARTES CRISTÃS": "QUIERO LAS ARTES CRISTIANAS",
 "MENOS COMPLICAÇÃO, MAIS PRODUÇÃO E MUITO MAIS PRATICIDADE": "MENOS COMPLICACIÓN, MÁS PRODUCCIÓN Y MUCHA MÁS PRACTICIDAD",
 "Mais rapidez na produção": "Más rapidez en la producción",
 "Você economiza horas usando modelos já prontos para CNC e laser.": "Ahorras horas usando modelos ya listos para CNC y láser.",
 "Produza mais peças sem se sobrecarregar": "Produce más piezas sin sobrecargarte",
 "Com arquivos prontos, você agiliza pedidos e produz muito mais rápido.": "Con archivos listos, agilizas pedidos y produces mucho más rápido.",
 "Mais segurança no corte": "Más seguridad en el corte",
 "Os arquivos já estão organizados e prontos para usar na máquina.": "Los archivos ya están organizados y listos para usar en la máquina.",
 "Mais autonomia na produção": "Más autonomía en la producción",
 "Você resolve tudo sozinho sem depender de terceiros para criar artes.": "Resuelves todo por tu cuenta sin depender de terceros para crear artes.",
 "Arquivos prontos para cortar, vender e personalizar:": "Archivos listos para cortar, vender y personalizar:",
 "APROVEITE O PREÇO PROMOCIONAL POR TEMPO LIMITADO": "APROVECHA EL PRECIO PROMOCIONAL POR TIEMPO LIMITADO",
 "Minutos": "Minutos",
 "Segundos": "Segundos",
 "QUANTO TEMPO E PRODUÇÃO VOCÊ ESTÁ PERDENDO POR NÃO TER ESSES ARQUIVOS PRONTOS?": "¿CUÁNTO TIEMPO Y PRODUCCIÓN ESTÁS PERDIENDO POR NO TENER ESTOS ARCHIVOS LISTOS?",
 "Produza mais peças em menos tempo": "Produce más piezas en menos tiempo",
 "Agilize seus pedidos sem complicação": "Agiliza tus pedidos sin complicación",
 "Trabalhe com menos retrabalho e estresse": "Trabaja con menos retrabajo y estrés",
 "QUERO ACESSAR AGORA E USAR HOJE": "QUIERO ACCEDER AHORA Y USAR HOY",
 "ESSE MATERIAL É IDEAL PARA VOCÊ QUE...": "ESTE MATERIAL ES IDEAL PARA TI QUE...",
 "QUER PRODUZIR MAIS E PARAR DE CRIAR ARTES DO ZERO": "QUIERES PRODUCIR MÁS Y DEJAR DE CREAR ARTES DESDE CERO",
 "Os pedidos chegam o tempo todo, e criar cada arte manualmente só atrasa sua produção. Com modelos prontos, você corta e entrega muito mais rápido.": "Los pedidos llegan todo el tiempo, y crear cada arte manualmente solo retrasa tu producción. Con modelos listos, cortas y entregas mucho más rápido.",
 "PRECISA PRODUZIR PEDIDOS COM MAIS AGILIDADE": "NECESITAS PRODUCIR PEDIDOS CON MÁS AGILIDAD",
 "Peças simples também tomam tempo quando você precisa criar tudo do zero. Aqui você produz mais rápido sem complicação.": "Las piezas simples también toman tiempo cuando necesitas crear todo desde cero. Aquí produces más rápido sin complicación.",
 "NÃO SABE CRIAR ARTES, MAS QUER PEÇAS COM VISUAL PROFISSIONAL": "NO SABES CREAR ARTES, PERO QUIERES PIEZAS CON ASPECTO PROFESIONAL",
 "Os modelos já estão prontos para usar. Você só escolhe, corta e produz peças com aparência profissional.": "Los modelos ya están listos para usar. Solo eliges, cortas y produces piezas con apariencia profesional.",
 "TEM MEDO DE PERDER MATERIAL COM ARQUIVOS ERRADOS": "TIENES MIEDO DE PERDER MATERIAL CON ARCHIVOS EQUIVOCADOS",
 "Os arquivos já estão organizados e prontos para CNC e laser, evitando retrabalho e desperdício de material.": "Los archivos ya están organizados y listos para CNC y láser, evitando retrabajo y desperdicio de material.",
 "Tudo o que você vai receber": "Todo lo que vas a recibir",
 "⚡ACESSO IMEDIATO": "⚡ACCESO INMEDIATO",
 "+50 artes cristãs premium prontas para CNC e laser": "+50 artes cristianas premium listas para CNC y láser",
 "Arquivos em DXF, SVG e AI": "Archivos en DXF, SVG y AI",
 "Modelos organizados por categorias": "Modelos organizados por categorías",
 "Arquivos prontos para corte imediato": "Archivos listos para corte inmediato",
 "Peças modernas e profissionais": "Piezas modernas y profesionales",
 "Artes pensadas para produção rápida": "Artes pensadas para producción rápida",
 "Capas pensadas para quem não é designer": "Diseños pensados para quien no es diseñador",
 "Modelos fáceis de usar mesmo sem experiência": "Modelos fáciles de usar incluso sin experiencia",
 "Download imediato após a compra": "Descarga inmediata tras la compra",
 "E NÃO PARA POR AÍ...": "Y NO PARA AHÍ...",
 "TEM MAIS!": "¡HAY MÁS!",
 "Você também vai receber…": "También vas a recibir…",
 "🔥 5 BÔNUS EXCLUSIVOS": "🔥 5 BONOS EXCLUSIVOS",
 "BÔNUS #1": "BONO #1",
 "Pack de Chaveiros Religiosos para Laser": "Pack de Llaveros Religiosos para Láser",
 "Modelos prontos de chaveiros religiosos para produzir peças rápidas, fáceis de vender e perfeitas para lembrancinhas e presentes.": "Modelos listos de llaveros religiosos para producir piezas rápidas, fáciles de vender y perfectas para recuerdos y regalos.",
 "Valor:": "Valor:",
 "GRÁTIS": "GRATIS",
 "BÔNUS #2": "BONO #2",
 "Pack de Luminárias Religiosas": "Pack de Lámparas Religiosas",
 "Coleção de luminárias religiosas modernas em camadas para criar peças premium com alto valor percebido.": "Colección de lámparas religiosas modernas en capas para crear piezas premium con alto valor percibido.",
 "BÔNUS #3": "BONO #3",
 "Pack de Topos de Bolo de Primeira Comunhão": "Pack de Toppers de Pastel de Primera Comunión",
 "Arquivos prontos para produzir topos de bolo religiosos para festas, eventos e lembranças especiais.": "Archivos listos para producir toppers de pastel religiosos para fiestas, eventos y recuerdos especiales.",
 "Pack de Caixas em MDF": "Pack de Cajas en MDF",
 "Modelos modernos de caixas para CNC e laser, ideais para decoração, presentes e vendas no dia a dia.": "Modelos modernos de cajas para CNC y láser, ideales para decoración, regalos y ventas del día a día.",
 "Pack de Porta-Chaves Decorativos para CNC": "Pack de Porta-Llaves Decorativos para CNC",
 "Coleção de porta-chaves decorativos modernos e fáceis de produzir para ampliar seu catálogo de produtos.": "Colección de porta-llaves decorativos modernos y fáciles de producir para ampliar tu catálogo de productos.",
 "⏰ ÚLTIMA CHANCE — OFERTA TERMINA HOJE": "⏰ ÚLTIMA OPORTUNIDAD — LA OFERTA TERMINA HOY",
 "Escolha a opção ideal para a sua rotina:": "Elige la opción ideal para tu rutina:",
 "Plano básico": "Plan básico",
 "+50 Artes Cristãs Premium": "+50 Artes Cristianas Premium",
 "Arquivos prontos para CNC e Laser": "Archivos listos para CNC y Láser",
 "Download imediato": "Descarga inmediata",
 "de R$47,90 por:": "de R$47,90 por:",
 "ou 4x de R$5,01 no cartão": "o 4x de R$5,01 en la tarjeta",
 "Você economiza": "Ahorras",
 "QUERO SOMENTE O BÁSICO": "QUIERO SOLO EL BÁSICO",
 "92% das pessoas aproveitam a oferta abaixo:": "92% de las personas aprovechan la oferta de abajo:",
 "⚡MAIS VENDIDO": "⚡MÁS VENDIDO",
 "PLANO COMPLETO": "PLAN COMPLETO",
 "⚡2x mais conteúdos": "⚡2x más contenidos",
 "Compatível com Aspire e ArtCAM": "Compatible con Aspire y ArtCAM",
 "🎁 Bônus #1 Pack de Chaveiros Religiosos": "🎁 Bono #1 Pack de Llaveros Religiosos",
 "🎁 Bônus #2 Luminárias Religiosas 3D": "🎁 Bono #2 Lámparas Religiosas 3D",
 "🎁 Bônus #3 Topos de Bolo Primeira Comunhão": "🎁 Bono #3 Toppers de Pastel Primera Comunión",
 "🎁 Bônus #4 Caixas Organizadoras MDF": "🎁 Bono #4 Cajas Organizadoras MDF",
 "🎁 Bônus #5 Porta-Chaves Decorativos": "🎁 Bono #5 Porta-Llaves Decorativos",
 "Acesso imediato": "Acceso inmediato",
 "ou 6x de R$13,35 no cartão": "o 6x de R$13,35 en la tarjeta",
 "QUERO O PLANO COMPLETO": "QUIERO EL PLAN COMPLETO",
 "GARANTIA DE 15 DIAS — ZERO RISCO PRA VOCÊ": "GARANTÍA DE 15 DÍAS — CERO RIESGO PARA TI",
 "Você não precisa comprar no escuro.": "No necesitas comprar a ciegas.",
 "Após a compra, você terá 15 dias para acessar os arquivos, testar os modelos, verificar a compatibilidade com sua máquina e produzir suas peças com calma.": "Tras la compra, tendrás 15 días para acceder a los archivos, probar los modelos, verificar la compatibilidad con tu máquina y producir tus piezas con calma.",
 "Se por qualquer motivo você sentir que o material não é pra você, basta solicitar o reembolso dentro do prazo.": "Si por cualquier motivo sientes que el material no es para ti, basta con solicitar el reembolso dentro del plazo.",
 "Sem burocracia.": "Sin burocracia.",
 "Sem complicação.": "Sin complicación.",
 "Sem risco.": "Sin riesgo.",
 "O risco fica com a gente, não com você.": "El riesgo es nuestro, no tuyo.",
 "Perguntas Frequentes": "Preguntas Frecuentes",
 "ESSES ARQUIVOS FUNCIONAM NA MINHA MÁQUINA?": "¿ESTOS ARCHIVOS FUNCIONAN EN MI MÁQUINA?",
 "Sim. Os arquivos são compatíveis com máquinas CNC Router, Laser e softwares como Aspire, ArtCAM e similares.": "Sí. Los archivos son compatibles con máquinas CNC Router, Láser y software como Aspire, ArtCAM y similares.",
 "COMO RECEBO OS ARQUIVOS APÓS A COMPRA?": "¿CÓMO RECIBO LOS ARCHIVOS TRAS LA COMPRA?",
 "O acesso é imediato. Após a confirmação do pagamento, você recebe o link da área de membros diretamente no seu e-mail.": "El acceso es inmediato. Tras la confirmación del pago, recibes el enlace del área de miembros directamente en tu correo.",
 "OS ARQUIVOS JÁ ESTÃO PRONTOS PARA USO?": "¿LOS ARCHIVOS YA ESTÁN LISTOS PARA USAR?",
 "Sim. Os modelos já estão organizados e prontos para corte, facilitando sua produção desde o primeiro acesso.": "Sí. Los modelos ya están organizados y listos para cortar, facilitando tu producción desde el primer acceso.",
 "PRECISO PAGAR MENSALIDADE?": "¿NECESITO PAGAR MENSUALIDAD?",
 "Não. O pagamento é único e o acesso ao material é liberado imediatamente após a compra.": "No. El pago es único y el acceso al material se libera inmediatamente tras la compra.",
 "E SE EU NÃO GOSTAR?": "¿Y SI NO ME GUSTA?",
 "Você terá 7 dias de garantia para acessar o material e testar tudo sem risco.": "Tendrás 7 días de garantía para acceder al material y probar todo sin riesgo.",
 "Copyright ©  2026 |  Todos os direitos reservados.": "Copyright ©  2026 |  Todos los derechos reservados.",
 "Este site não é afiliado ao Facebook™, Instagram™, Google™ ou qualquer outra plataforma mencionada.": "Este sitio no está afiliado a Facebook™, Instagram™, Google™ ni ninguna otra plataforma mencionada.",
 "Todos os direitos sobre a obra": "Todos los derechos sobre la obra",
 "são reservados ao próprio produto, nos termos da Lei nº 9.610/98 (Lei de Direitos Autorais).": "están reservados al propio producto, conforme a la Ley n.º 9.610/98 (Ley de Derechos de Autor).",
 "A reprodução não autorizada desta publicação, no todo ou em parte, por quaisquer meios, constitui violação dos direitos autorais (Art. 184 do Código Penal e Lei 9.610/98), sujeitando os infratores às sanções civis e criminais previstas na legislação aplicável.": "La reproducción no autorizada de esta publicación, total o parcialmente, por cualquier medio, constituye una violación de los derechos de autor (Art. 184 del Código Penal y Ley 9.610/98), sujetando a los infractores a las sanciones civiles y penales previstas en la legislación aplicable.",
 "Update": "Actualizar",
 "Browser": "Navegador",
 "We use cookies to enhance your browsing experience, provide personalized content, and improve site performance. For the best experience, please keep your browser up to date —": "Usamos cookies para mejorar tu experiencia de navegación, ofrecer contenido personalizado y mejorar el rendimiento del sitio. Para una mejor experiencia, mantén tu navegador actualizado —",
 "download browser version": "descarga la versión del navegador",
 "Accept": "Aceptar",
 "Reject": "Rechazar",
}

# attribute-based strings (meta tags, alt, aria) to translate
ATTR = {
 "Artes Cristas – arquivoscnc.online": "Artes Cristianas – arquivoscnc.online",
 "Artes Cristas": "Artes Cristianas",
}

src = open(BASE, encoding="utf-8").read()

# Mask <script> and <style> so we never touch their contents
masks = []
def mask(m):
    masks.append(m.group(0))
    return f"\x00{len(masks)-1}\x00"
masked = re.sub(r"<(script|style)\b.*?</\1>", mask, src, flags=re.S|re.I)

esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
hits = {"text":0, "miss":set()}

def repl_text(m):
    inner = m.group(1)
    stripped = html.unescape(inner).strip()
    if stripped in T:
        lead = inner[:len(inner)-len(inner.lstrip())]
        trail = inner[len(inner.rstrip()):]
        hits["text"] += 1
        return ">" + lead + esc(T[stripped]) + trail + "<"
    return m.group(0)

masked = re.sub(r">([^<>]+)<", repl_text, masked)

# meta/og/twitter content + title attributes
def repl_attr(m):
    pre, val, post = m.group(1), m.group(2), m.group(3)
    dec = html.unescape(val).strip()
    if dec in ATTR:
        return pre + esc(ATTR[dec]) + post
    if dec in T:
        return pre + esc(T[dec]) + post
    return m.group(0)
masked = re.sub(r'(content=")([^"]*)(")', repl_attr, masked)

# restore masks
out = re.sub(r"\x00(\d+)\x00", lambda m: masks[int(m.group(1))], masked)

open(BASE, "w", encoding="utf-8").write(out)
print("text nodes translated:", hits["text"])
