from transformers import BertPreTrainedModel, BertModel
import torch.nn as nn
import torch

class BertWithLexicon(BertPreTrainedModel):
    def __init__(self, config, num_dialects):
        super().__init__(config)
        self.bert = BertModel(config)
        self.dropout = nn.Dropout(p=0.3)
        self.fc = nn.Linear(config.hidden_size + num_dialects, config.hidden_size)
        self.classifier = nn.Linear(config.hidden_size, config.num_labels)
        self.init_weights()

    def forward(self, input_ids, attention_mask=None, token_type_ids=None, position_ids=None, head_mask=None, inputs_embeds=None, labels=None, dialect_features=None):
        outputs = self.bert(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
        )

        pooled_output = outputs[1]
        pooled_output = self.dropout(pooled_output)

        combined_output = torch.cat((pooled_output, dialect_features), dim=1)
        combined_output = self.fc(combined_output)
        combined_output = self.dropout(combined_output)

        logits = self.classifier(combined_output)

        loss = None
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(logits.view(-1, self.config.num_labels), labels.view(-1))

        return {
            'loss': loss,
            'logits': logits
        }
