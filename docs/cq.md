## Competency Questions

DoCO can be used for answering several questions related to documents and their structural and rethorical elements.

In the following subsections, some of them are introduced together with their respective SPARQL queries. 

The prefixes that are used in all the SPARQL queries provided below are defined as follows:

    PREFIX : <http://www.sparontologies.net/example/> 
    PREFIX doco: <http://purl.org/spar/doco/>
    PREFIX deo: <http://purl.org/spar/deo/>
    PREFIX po: <http://www.essepuntato.it/2008/12/pattern#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX fabio: <http://purl.org/spar/fabio/>
    PREFIX co: <http://purl.org/co/>
    PREFIX c4o: <http://purl.org/spar/c4o>

### CQ1

What are all the sections contained within the article's body matter, and in which sequential order do they appear?

    SELECT ?section ?sectionType
    WHERE {
        ?bodyMatter a doco:BodyMatter ;
                    co:firstItem ?item .
        
        ?item co:itemContent ?section .
        ?item co:nextItem* ?next .
        ?next co:itemContent ?section .
        
        OPTIONAL { ?section a ?sectionType . }
    }

### CQ2

What is the literal textual content of the first sentence belonging to the first paragraph of the introduction section?

    SELECT ?sentenceText
    WHERE {
        ?introSection a deo:Introduction .
        
        ?introSection co:firstItem ?headerItem .
        ?headerItem co:nextItem ?firstParagraphItem .
        ?firstParagraphItem co:itemContent ?firstParagraph .
        ?firstParagraph a doco:Paragraph .
        
        ?firstParagraph co:firstItem ?firstSentenceItem .
        ?firstSentenceItem co:itemContent ?firstSentence .
        
        ?firstSentence c4o:hasContent ?sentenceText .
    }

### CQ3

Which in-text references are contained within a specific sentence, and what are their literal textual markers?

    SELECT ?reference ?textMarker
    WHERE {
        ?sentence a doco:Sentence ;
                po:contains ?reference .
        
        ?reference c4o:hasContent ?textMarker .
    }

### CQ4

What is the full bibliographic text of the reference cited by a specific inline citation marker?

    SELECT ?inlineMarker ?fullBibliographicText
    WHERE {
        ?reference a deo:Reference ;
                c4o:hasContent ?inlineMarker ;
                dcterms:references ?bibReference .
        
        ?bibReference a deo:BibliographicReference ;
                    c4o:hasContent ?fullBibliographicText .
    }