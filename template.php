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
Dieser Artikel wurde von einer künstlichen Intelligenz geschrieben! Er dient als 
Demonstrationsbeispiel für automatisiert erzeugte Inhalte. Der Artikel kann
Unsinn und falsche Aussagen enthalten!
</p>
</div>
</section>

{CONTENT}

<?php 
	$page->build_html_bottom(__FILE__); 
?> 