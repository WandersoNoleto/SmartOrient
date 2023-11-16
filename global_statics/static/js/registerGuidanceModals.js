    // Src: registerGuidace.html

    // Capturar o valor selecionado no modal e preencher no input de Orientador
    function selectAdvisor(advisorName, inputId) {
        $('#advisorsModal').modal('hide');
        $('#' + inputId).val(advisorName);
      }
  
      $(document).on('click', '.advisor-row', function() {
        var advisorName = $(this).find('.advisor-name').text();
        selectAdvisor(advisorName, 'advisor');
      });
  
      // Capturar o valor selecionado no modal e preencher no input de Coordenação
      function selectCoordination(coordinationCode, inputId) {
          $('#coordModal').modal('hide');
          $('#' + inputId).val(coordinationCode);
          }
      
          $(document).on('click', '.coord-row', function() {
            var coordinationCode = $(this).find('.coord-code').text();
            selectCoordination(coordinationCode, 'coordination');
          });