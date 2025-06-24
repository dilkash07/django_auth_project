import * as z from "zod";

export const forgotPasswordSchema = z.object({
  email: z.string().email("Invalid email"),
});

export type ForgotPasswordFormValue = z.infer<typeof forgotPasswordSchema>;
