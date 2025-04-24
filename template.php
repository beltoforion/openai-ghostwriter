<?php
	include ("pagebuilder.php");

	$page->page_title = '{TOPIC}';
	$page->subtitle = 'Dieser Artikel wurde von einer künstlichen Intelligenz geschrieben!';
 ?> 

<!DOCTYPE HTML>

<html>
	<head>
		<title>{TOPIC}</title>
		<meta charset="utf-8" />
		<meta name="robots" content="noindex">		
		<?php $page->include_dependencies('../../..'); ?>
	</head>
	<body class="is-preload">
		<!-- Wrapper -->
			<div id="wrapper">

				<!-- Main -->
					<div id="main">
						<div class="inner">

							<!-- Header -->
							<?php $page->build_header(); ?>

<section>
<div class="box" style="background:#ffff00; color:red;" >
<p>
This article may contain factual errors. It was created by 
the <a href="https://github.com/beltoforion/openai-ghostwriter">openai-ghostwriter {VERSION}</a> using the {MODEL} model. 
This is a python script for automatic generation of web pages powered by the OpenAI's GPT-3.
</p>

<hr>

<p>
Dieser Artikel kann Unsinn und falsche Aussagen enthalten! Er wurde vom 
<a href="https://github.com/beltoforion/openai-ghostwriter">openai-ghostwriter {VERSION}</a> erzeugt. Das
ist ein Python-Skript für die vollautomatische Erstellung von Webseiten. 
</p>
</div>
</section>

{CONTENT}

<?php 
	$page->build_html_bottom(__FILE__); 
?> 