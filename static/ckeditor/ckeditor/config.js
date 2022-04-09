/**
 * @license Copyright (c) 2003-2021, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	config.allowedContent = true;
};

CKEDITOR.on( 'instanceReady', function( evt ) {
	evt.editor.dataProcessor.htmlFilter.addRules( {
	  elements: {
		h2: function(el) {
		  el.addClass('article-body-title');
		}, 
		h3: function(el) {
			el.addClass('article-body-title');
		}
	  }
	});
  });