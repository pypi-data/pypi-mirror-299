"""Implementation of a resnet18 model as a custom model."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Optional, Union, cast

import torch
from torch import Tensor
import torch.nn as nn
from torch.nn import functional as F
import torch.optim as optimizers
from torch.optim.lr_scheduler import _LRScheduler
import torch_optimizer as torch_optimizers

from bitfount import (  # type: ignore[attr-defined] # Reason: BIT-2475
    BitfountDataLoader,
    PyTorchBitfountModel,
)
from bitfount.backends.pytorch.data.dataloaders import PyTorchDataLoader
from bitfount.backends.pytorch.models.base_models import PyTorchClassifierMixIn
from bitfount.backends.pytorch.models.nn import _get_torchvision_classification_model
from bitfount.backends.pytorch.types import (
    ImgAndTabBatch,
    ImgAndTabDataSplit,
    ImgDataReturnType,
    ImgFwdTypes,
    ImgXorTabBatch,
    ImgXorTabDataSplit,
    TabDataReturnType,
)
from bitfount.data.datasources.base_source import BaseSource
from bitfount.types import PredictReturnType

_OptimizerType = Union[torch_optimizers.Optimizer, optimizers.Optimizer]


class DmeCnvOctModel(PyTorchClassifierMixIn, PyTorchBitfountModel):
    """Implementation of a resnet18 model as a custom model."""

    def __init__(
        self,
        batch_size: int = 4,
        n_classes: int = 4,
        slo_included: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.batch_size = batch_size
        self.n_classes = n_classes
        self.slo_included = slo_included

    def _split_dataloader_output(
        self,
        data: Union[ImgAndTabDataSplit, ImgXorTabDataSplit],
    ) -> Union[ImgDataReturnType, TabDataReturnType]:
        """Splits dataloader output into image tensor, weights and category."""
        images, sup = cast(tuple[torch.Tensor, torch.Tensor], data)
        weights = sup[:, 0].float()
        category: Optional[torch.Tensor]
        if sup.shape[1] > 2:
            category = sup[:, -1:].long()
        else:
            category = None

        return images, weights, category

    def create_model(self) -> nn.Module:
        """Creates the model to use."""
        model = _get_torchvision_classification_model(
            model_name="resnet18", pretrained=True, num_classes=self.n_classes
        )
        return model

    def configure_optimizers(
        self,
    ) -> Union[_OptimizerType, tuple[list[_OptimizerType], list[_LRScheduler]]]:
        """Configures the optimizer(s) and scheduler(s) for backpropagation.

        Returns:
            Either the optimizer of your choice or a tuple of optimizers and learning
            rate schedulers.
        """
        parameters = filter(lambda p: p.requires_grad, self.parameters())
        optimizer: _OptimizerType = self._opt_func(parameters)
        if self._scheduler_func:
            scheduler = self._scheduler_func(optimizer)
            return [optimizer], [scheduler]

        return optimizer

    def forward(self, x: ImgFwdTypes) -> Any:
        """Performs a forward pass of the model."""
        # override as the forward function is incompatible with pl.LightningModule
        if self.datastructure.number_of_images > 1:
            aux = []
            for i in range(len(x)):
                aux.append(self._model(x[i]))
            return torch.cat([item[0] for item in aux], 1)
        else:
            return self._model(x)

    @staticmethod
    def _handle_categories_or_tuple(
        output: Union[torch.Tensor, tuple[torch.Tensor, torch.Tensor]],
        categories: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Handles conversion of output if categorical or tensor."""
        if categories is not None:
            # get output corresponding to right head depending on label
            categories = categories.unsqueeze(dim=1)
            output_to_stack: tuple[Tensor, ...]
            if not isinstance(output, tuple):
                output_to_stack = (output,)
            else:
                output_to_stack = output
            stacked_output = torch.stack(output_to_stack, 1)
            categories = categories.expand_as(stacked_output)
            output = stacked_output.gather(1, categories)[:, 1]
        # Handle tuple output
        elif isinstance(output, tuple):
            output = output[0]
        return output

    def _do_output_activation(self, output: torch.Tensor) -> torch.Tensor:
        """Perform final activation function on output."""
        if self.multilabel:
            return torch.sigmoid(output)
        else:
            return F.softmax(output, dim=1)

    def training_step(self) -> None:
        """Not implemented since this model is only being used for inference."""
        ...

    def validation_step(self) -> None:
        """Not implemented since this model is only being used for inference."""
        ...

    def test_step(
        self,
        batch: Union[
            tuple[Union[ImgXorTabBatch, ImgAndTabBatch], torch.Tensor],
            tuple[Union[ImgXorTabBatch, ImgAndTabBatch], torch.Tensor, Sequence[str]],
        ],
        batch_idx: int,
    ) -> dict[str, Any]:
        """Make sure to set self.preds and self.target before returning in this method.

        They will be returned by the `evaluate` method.

        Args:
            batch: The batch to be evaluated.
            batch_idx: The index of the batch to be evaluated from the test
                dataloader.

        Returns:
            A dictionary of predictions and targets. These will be passed to the
            `test_epoch_end` method.
        """
        # Extract X, y and other data from batch
        data, y = batch[:2]

        # If the data provides data keys, extract those as well
        keys: Optional[list[str]] = None
        if self._expect_keys(self.trainer.test_dataloaders):
            batch = cast(
                tuple[
                    Union[ImgXorTabBatch, ImgAndTabBatch], torch.Tensor, Sequence[str]
                ],
                batch,
            )
            keys = list(batch[2])

        x, *loss_modifiers = self._split_dataloader_output(data)

        # Get validation output and loss
        y_hat = self(x)

        # Handle categorical or tuple output
        categories = loss_modifiers[-1]
        y_hat = self._handle_categories_or_tuple(y_hat, categories)

        y_hat = self._do_output_activation(y_hat)

        # Output targets and prediction for later
        if keys is not None:
            return {"predictions": y_hat, "targets": y, "keys": keys}
        else:
            return {"predictions": y_hat, "targets": y}

    def _predict_local(self, data: BaseSource, **kwargs: Any) -> PredictReturnType:
        """This method runs inference on the test data, returns predictions.

        This is done by calling `test_step` under the hood. Customise this method as you
        please but it must return a list of predictions and a list of targets. Note that
        as this is the prediction function, only the predictions are returned.

        Returns:
            A numpy array containing the prediction values.
        """
        if data is not None:
            data.load_data()
            if not hasattr(self, "databunch"):
                self._add_datasource_to_schema(data)  # Also sets `self.databunch`
            if not self.databunch:
                self._add_datasource_to_schema(data)  # Also sets `self.databunch
            test_dl = self.databunch.get_test_dataloader(self.batch_size)
            if not isinstance(test_dl, BitfountDataLoader):
                raise ValueError("No test data to infer in the provided datasource.")

        self._pl_trainer.test(model=self, dataloaders=cast(PyTorchDataLoader, test_dl))

        if self._test_preds is not None:
            return PredictReturnType(preds=self._test_preds, keys=self._test_keys)

        raise ValueError("'self._test_preds' was not set by the model after inference.")
